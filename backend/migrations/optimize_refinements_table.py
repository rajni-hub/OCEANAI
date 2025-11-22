"""
Migration script to optimize refinements table by removing content columns.

This migration:
1. Removes previous_content and new_content columns from refinements table
2. Creates new feedback table for likes/dislikes
3. Migrates existing feedback data to new table
4. Adds indexes for performance
5. Limits refinement history to last 3 per section

Run this script manually or via Alembic.
"""

import sys
import os
import uuid as uuid_module
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings


def migrate_refinements_table():
    """
    Migrate refinements table to remove content columns and create feedback table.
    """
    database_url = settings.DATABASE_URL
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        inspector = inspect(engine)
        
        # Check if refinements table exists
        if 'refinements' not in inspector.get_table_names():
            print("❌ Refinements table does not exist. Skipping migration.")
            return
        
        # Get current columns
        columns = [col['name'] for col in inspector.get_columns('refinements')]
        print(f"Current columns in refinements table: {columns}")
        
        # Step 1: Create feedback table if it doesn't exist
        print("\n[1/5] Creating feedback table...")
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS feedback (
                id VARCHAR(36) PRIMARY KEY,
                document_id VARCHAR(36) NOT NULL,
                section_id VARCHAR(100) NOT NULL,
                feedback_type VARCHAR(20) NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
            )
        """))
        
        # Create indexes for feedback table
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_feedback_document_id 
            ON feedback(document_id)
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_feedback_section_id 
            ON feedback(section_id)
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_feedback_document_section 
            ON feedback(document_id, section_id)
        """))
        conn.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_feedback_unique_section 
            ON feedback(document_id, section_id)
        """))
        print("✅ Feedback table created with indexes")
        
        # Step 2: Migrate existing feedback data from refinements to feedback table
        print("\n[2/5] Migrating existing feedback data...")
        conn.execute(text("""
            INSERT OR IGNORE INTO feedback (id, document_id, section_id, feedback_type, created_at, updated_at)
            SELECT 
                lower(hex(randomblob(4)) || '-' || hex(randomblob(2)) || '-4' || 
                      substr(hex(randomblob(2)), 2) || '-' || 
                      substr('89ab', abs(random()) % 4 + 1, 1) || 
                      substr(hex(randomblob(2)), 2) || '-' || hex(randomblob(6))),
                document_id,
                section_id,
                feedback,
                created_at,
                created_at
            FROM refinements
            WHERE feedback IS NOT NULL
            GROUP BY document_id, section_id
            HAVING MAX(created_at) = created_at
        """))
        print("✅ Feedback data migrated")
        
        # Step 3: Add indexes to refinements table if they don't exist
        print("\n[3/5] Adding indexes to refinements table...")
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_refinement_document_section 
                ON refinements(document_id, section_id)
            """))
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_refinement_section_created 
                ON refinements(section_id, created_at)
            """))
            print("✅ Indexes added")
        except Exception as e:
            print(f"⚠️  Index creation warning (may already exist): {e}")
        
        # Step 4: Remove content columns (SQLite doesn't support DROP COLUMN directly)
        print("\n[4/5] Removing content columns...")
        if 'previous_content' in columns or 'new_content' in columns:
            # SQLite doesn't support DROP COLUMN, so we need to recreate the table
            print("⚠️  SQLite detected - recreating table without content columns...")
            
            # Create new table structure
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS refinements_new (
                    id VARCHAR(36) PRIMARY KEY,
                    document_id VARCHAR(36) NOT NULL,
                    section_id VARCHAR(100) NOT NULL,
                    refinement_prompt TEXT,
                    feedback VARCHAR(20),
                    comments TEXT,
                    created_at DATETIME NOT NULL,
                    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
                )
            """))
            
            # Copy data (excluding content columns)
            conn.execute(text("""
                INSERT INTO refinements_new 
                (id, document_id, section_id, refinement_prompt, feedback, comments, created_at)
                SELECT 
                    id, document_id, section_id, refinement_prompt, feedback, comments, created_at
                FROM refinements
            """))
            
            # Drop old table
            conn.execute(text("DROP TABLE refinements"))
            
            # Rename new table
            conn.execute(text("ALTER TABLE refinements_new RENAME TO refinements"))
            
            # Recreate indexes
            conn.execute(text("""
                CREATE INDEX idx_refinement_document_id ON refinements(document_id)
            """))
            conn.execute(text("""
                CREATE INDEX idx_refinement_section_id ON refinements(section_id)
            """))
            conn.execute(text("""
                CREATE INDEX idx_refinement_document_section 
                ON refinements(document_id, section_id)
            """))
            conn.execute(text("""
                CREATE INDEX idx_refinement_section_created 
                ON refinements(section_id, created_at)
            """))
            
            print("✅ Content columns removed")
        else:
            print("✅ Content columns already removed")
        
        # Step 5: Limit refinement history to last 3 per section
        print("\n[5/5] Limiting refinement history...")
        conn.execute(text("""
            DELETE FROM refinements
            WHERE id IN (
                SELECT id FROM (
                    SELECT id, 
                           ROW_NUMBER() OVER (
                               PARTITION BY document_id, section_id 
                               ORDER BY created_at DESC
                           ) as rn
                    FROM refinements
                ) WHERE rn > 3
            )
        """))
        print("✅ Refinement history limited to last 3 per section")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")


if __name__ == "__main__":
    print("=" * 60)
    print("Refinements Table Optimization Migration")
    print("=" * 60)
    print("\nThis migration will:")
    print("  1. Create feedback table")
    print("  2. Migrate existing feedback data")
    print("  3. Add performance indexes")
    print("  4. Remove content columns from refinements table")
    print("  5. Limit refinement history to last 3 per section")
    print("\n⚠️  WARNING: This will remove previous_content and new_content columns!")
    print("   Content is now stored only in documents.content")
    print("\n" + "=" * 60)
    
    response = input("\nContinue with migration? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled.")
        sys.exit(0)
    
    try:
        migrate_refinements_table()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

