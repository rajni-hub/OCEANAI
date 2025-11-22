import { useState, useEffect, useRef } from "react";
import { refinementAPI } from "../services/api";
import "./RefinementInterface.css";

const RefinementInterface = ({ project, document, onUpdate }) => {
  // 🔥 MOUNT TRACKING - Check if component is being remounted
  useEffect(() => {
    console.log("🔥 RefinementInterface MOUNTED");
    console.trace("🔥 MOUNT STACK TRACE");
    return () => {
      console.log("🔥 RefinementInterface UNMOUNTED");
      console.trace("🔥 UNMOUNT STACK TRACE");
    };
  }, []);
  const [selectedItem, setSelectedItem] = useState(null);
  const [refinementPrompt, setRefinementPrompt] = useState("");
  const [comments, setComments] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [content, setContent] = useState(document?.content || {});
  // Track feedback for each section: { sectionId: "like" | "dislike" | null }
  const [sectionFeedback, setSectionFeedback] = useState({});

  // Preserve selected item ID across ALL updates - this is the source of truth
  const selectedItemIdRef = useRef(null);
  const isRefiningRef = useRef(false); // Track if we're in the middle of a refinement

  // Preserve scroll position
  const scrollPositionRef = useRef(0);
  const contentDisplayRef = useRef(null);
  const refinementContentRef = useRef(null);
  const sidebarRef = useRef(null);
  const sidebarScrollRef = useRef(0);

  // Track if component has been initialized (prevents re-initialization)
  const isInitializedRef = useRef(false);

  // Log selectedItem state changes - TRACE EVERY setSelectedItem CALL
  useEffect(() => {
    console.log("[STATE_TRACK] ============================================");
    console.log("[STATE_TRACK] selectedItem STATE CHANGED:");
    console.log(
      "[STATE_TRACK]   New selectedItem:",
      selectedItem ? { id: selectedItem.id, title: selectedItem.title } : "NULL"
    );
    console.log(
      "[STATE_TRACK]   selectedItemIdRef:",
      selectedItemIdRef.current
    );
    console.log("[STATE_TRACK]   isInitialized:", isInitializedRef.current);
    console.log("[STATE_TRACK]   isRefining:", isRefiningRef.current);
    console.log("[STATE_TRACK]   Stack trace:");
    console.trace("[STATE_TRACK]");
    console.log("[STATE_TRACK] ============================================");
  }, [selectedItem]);

  useEffect(() => {
    if (document) {
      const newContent = document.content || {};
      console.log(
        "[DOC_UPDATE] Document content updated, keys:",
        Object.keys(newContent)
      );
      setContent(newContent);
    }
  }, [document]);

  // Fetch existing feedback for all sections on mount and when document changes
  // Now using the optimized Feedback table instead of refinement history
  useEffect(() => {
    const fetchFeedback = async () => {
      if (!project || !document) return;

      try {
        // Fetch feedback from the optimized Feedback table
        const response = await refinementAPI.getFeedback(project.id);
        const feedbackData = response.data || {};

        // feedbackData is already a dictionary: { sectionId: "like" | "dislike" }
        setSectionFeedback(feedbackData);
        console.log("[FEEDBACK] Loaded feedback for sections:", feedbackData);
      } catch (err) {
        console.error("[FEEDBACK] Error fetching feedback:", err);
        // Don't show error to user - feedback is optional
        // Fallback: try to get from refinement history (for backward compatibility)
        try {
          const historyResponse = await refinementAPI.getRefinementHistory(
            project.id
          );
          const history = historyResponse.data?.refinements || [];
          const feedbackMap = {};
          history.forEach((refinement) => {
            if (refinement.feedback && refinement.section_id) {
              if (
                !feedbackMap[refinement.section_id] ||
                new Date(refinement.created_at) >
                  new Date(feedbackMap[refinement.section_id].created_at || 0)
              ) {
                feedbackMap[refinement.section_id] = {
                  feedback: refinement.feedback,
                  created_at: refinement.created_at,
                };
              }
            }
          });
          const feedbackState = {};
          Object.keys(feedbackMap).forEach((sectionId) => {
            feedbackState[sectionId] = feedbackMap[sectionId].feedback;
          });
          setSectionFeedback(feedbackState);
        } catch (fallbackErr) {
          console.error("[FEEDBACK] Fallback also failed:", fallbackErr);
        }
      }
    };

    fetchFeedback();
  }, [project, document]);

  const items =
    project.document_type === "word"
      ? document?.structure?.sections || []
      : document?.structure?.slides || [];
  const itemType = project.document_type === "word" ? "section" : "slide";

  // Initialize selection ONLY on first mount when items first become available
  // CRITICAL FIX: Only set first section if selectedItem is NULL
  // NEVER overwrite an existing selection
  useEffect(() => {
    console.log("[INIT_CHECK] ============================================");
    console.log("[INIT_CHECK] Initialization check triggered");
    console.log("[INIT_CHECK]   isInitialized:", isInitializedRef.current);
    console.log("[INIT_CHECK]   itemsLength:", items.length);
    console.log("[INIT_CHECK]   selectedItemIdRef:", selectedItemIdRef.current);
    console.log(
      "[INIT_CHECK]   selectedItem:",
      selectedItem ? { id: selectedItem.id, title: selectedItem.title } : "NULL"
    );
    console.log("[INIT_CHECK] ============================================");

    // CRITICAL FIX: If selectedItem exists, DO NOT overwrite it
    // This is the root cause - we were resetting even when selection existed
    if (selectedItem !== null) {
      console.log(
        "[INIT] 🛡️ BLOCKED - selectedItem exists, DO NOT overwrite:",
        {
          id: selectedItem.id,
          title: selectedItem.title,
        }
      );
      isInitializedRef.current = true;
      return; // Exit early - NEVER overwrite existing selection
    }

    // CRITICAL SAFEGUARD: Never initialize if we have a preserved selection ID
    if (selectedItemIdRef.current) {
      console.log(
        "[INIT] 🛡️ BLOCKED - selectedItemIdRef exists, DO NOT overwrite:",
        selectedItemIdRef.current
      );
      isInitializedRef.current = true;
      return; // Exit early - never initialize if selection exists
    }

    // Only initialize if:
    // 1. selectedItem is NULL (no current selection)
    // 2. selectedItemIdRef is NULL (no preserved selection)
    // 3. Items are available
    // 4. We haven't initialized yet
    if (
      !isInitializedRef.current &&
      items.length > 0 &&
      selectedItem === null &&
      !selectedItemIdRef.current
    ) {
      console.log("[INIT] ✅ Setting first item because selectedItem is NULL");
      console.log("[INIT]   Setting to:", {
        id: items[0].id,
        title: items[0].title,
      });
      selectedItemIdRef.current = items[0].id;
      setSelectedItem(items[0]);
      isInitializedRef.current = true;
    } else {
      console.log("[INIT] ❌ Skipping initialization:", {
        reason: !isInitializedRef.current
          ? "already initialized"
          : items.length === 0
          ? "no items"
          : selectedItem !== null
          ? "selectedItem exists"
          : selectedItemIdRef.current
          ? "selectedItemIdRef exists"
          : "unknown",
      });
      if (items.length > 0) {
        isInitializedRef.current = true;
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [items.length, selectedItem]); // Depend on selectedItem to prevent overwriting

  // Save scroll position before any updates
  useEffect(() => {
    const saveScrollPosition = () => {
      // Save main content scroll
      if (contentDisplayRef.current) {
        scrollPositionRef.current = contentDisplayRef.current.scrollTop;
      } else if (refinementContentRef.current) {
        scrollPositionRef.current = refinementContentRef.current.scrollTop;
      } else {
        scrollPositionRef.current = window.scrollY;
      }

      // Save sidebar scroll
      if (sidebarRef.current) {
        sidebarScrollRef.current = sidebarRef.current.scrollTop;
      }
    };

    // Save scroll position periodically and before updates
    const interval = setInterval(saveScrollPosition, 100);
    return () => clearInterval(interval);
  }, []);

  // Restore selection and scroll position when document updates (after refinement)
  // CRITICAL FIX: Only update if selectedItem is NULL or doesn't match the ref
  // NEVER overwrite an existing matching selection
  useEffect(() => {
    console.log("[RESTORE_CHECK] ============================================");
    console.log("[RESTORE_CHECK] Restoration check triggered");
    console.log("[RESTORE_CHECK]   isRefining:", isRefiningRef.current);
    console.log("[RESTORE_CHECK]   isInitialized:", isInitializedRef.current);
    console.log(
      "[RESTORE_CHECK]   selectedItemIdRef:",
      selectedItemIdRef.current
    );
    console.log("[RESTORE_CHECK]   itemsLength:", items.length);
    console.log(
      "[RESTORE_CHECK]   currentSelectedItem:",
      selectedItem ? { id: selectedItem.id, title: selectedItem.title } : "NULL"
    );
    console.log("[RESTORE_CHECK] ============================================");

    // Don't restore if we're currently refining (to avoid race conditions)
    if (isRefiningRef.current) {
      console.log(
        "[RESTORE] ⏸️ Skipping selection restore - refinement in progress"
      );
      return;
    }

    // CRITICAL FIX: Only restore if we have a preserved ID AND we're initialized
    // AND either selectedItem is NULL or it doesn't match the ref
    if (
      isInitializedRef.current &&
      selectedItemIdRef.current &&
      items.length > 0
    ) {
      const matchingItem = items.find(
        (item) => item.id === selectedItemIdRef.current
      );
      if (matchingItem) {
        // CRITICAL FIX: Check if selectedItem already matches - if so, DO NOT overwrite
        if (
          selectedItem !== null &&
          selectedItem.id === selectedItemIdRef.current
        ) {
          console.log(
            "[RESTORE] ✅ selectedItem already matches ref, DO NOT overwrite:",
            {
              id: selectedItem.id,
              title: selectedItem.title,
            }
          );
          // Selection is already correct, just restore scroll
          requestAnimationFrame(() => {
            if (contentDisplayRef.current) {
              contentDisplayRef.current.scrollTop = scrollPositionRef.current;
            } else if (refinementContentRef.current) {
              refinementContentRef.current.scrollTop =
                scrollPositionRef.current;
            }
            if (sidebarRef.current) {
              sidebarRef.current.scrollTop = sidebarScrollRef.current;
            }
          });
          return; // Exit early - don't overwrite existing matching selection
        }

        // Only update if selectedItem is NULL or doesn't match
        console.log("[RESTORE] ✅ Updating selection because:", {
          selectedItemIsNull: selectedItem === null,
          idsMatch: selectedItem?.id === selectedItemIdRef.current,
          reason:
            selectedItem === null
              ? "selectedItem is NULL"
              : "selectedItem does not match ref",
        });
        console.log("[RESTORE]   Restoring to:", {
          id: matchingItem.id,
          title: matchingItem.title,
        });

        // Save ALL scroll positions BEFORE updating selection
        const savedContentScroll =
          contentDisplayRef.current?.scrollTop ?? scrollPositionRef.current;
        const savedSidebarScroll =
          sidebarRef.current?.scrollTop ?? sidebarScrollRef.current;
        const savedWindowScroll = window.scrollY;

        console.log(
          "[RESTORE] Saving scroll positions before selection update:",
          {
            content: savedContentScroll,
            sidebar: savedSidebarScroll,
            window: savedWindowScroll,
          }
        );

        // Update selection WITHOUT causing scroll
        setSelectedItem(matchingItem);

        // CRITICAL: Immediately restore ALL scroll positions to prevent any jumps
        requestAnimationFrame(() => {
          // Restore content scroll
          if (contentDisplayRef.current) {
            contentDisplayRef.current.scrollTop = savedContentScroll;
          } else if (refinementContentRef.current) {
            refinementContentRef.current.scrollTop = savedContentScroll;
          }

          // Restore sidebar scroll - prevent auto-scroll to active item
          if (sidebarRef.current) {
            sidebarRef.current.scrollTop = savedSidebarScroll;
          }

          // Prevent window from scrolling
          if (Math.abs(window.scrollY - savedWindowScroll) > 5) {
            window.scrollTo({ top: savedWindowScroll, behavior: "instant" });
          }

          console.log("[RESTORE] All scroll positions restored:", {
            content: savedContentScroll,
            sidebar: savedSidebarScroll,
            window: savedWindowScroll,
          });
        });
      } else {
        console.warn(
          "[RESTORE] ⚠️ Selected item not found:",
          selectedItemIdRef.current,
          "Available items:",
          items.map((i) => i.id)
        );
        // If the selected item is not found, keep current selection if it exists
        // DO NOT reset to first item - this is the key fix
        if (selectedItem && selectedItem.id === selectedItemIdRef.current) {
          console.log(
            "[RESTORE] ✅ Keeping current selection:",
            selectedItem.title
          );
          // Selection is still valid, just keep it
        } else {
          console.warn(
            "[RESTORE] ⚠️ Current selection does not match ref, but NOT resetting to first item"
          );
        }
      }
    } else {
      console.log("[RESTORE] ❌ Skipping restoration - conditions not met:", {
        isInitialized: isInitializedRef.current,
        hasRef: !!selectedItemIdRef.current,
        hasItems: items.length > 0,
      });
    }

    // Restore scroll position after a brief delay to allow DOM to update
    const restoreScroll = () => {
      // CRITICAL: Prevent any automatic scrolling
      // Store current window scroll to prevent jumps
      const currentWindowScroll = window.scrollY;

      // Restore main content scroll
      if (contentDisplayRef.current) {
        contentDisplayRef.current.scrollTop = scrollPositionRef.current;
        console.log(
          "[RESTORE] Content scroll restored to:",
          scrollPositionRef.current
        );
      } else if (refinementContentRef.current) {
        refinementContentRef.current.scrollTop = scrollPositionRef.current;
        console.log(
          "[RESTORE] Refinement content scroll restored to:",
          scrollPositionRef.current
        );
      }

      // Restore sidebar scroll
      if (sidebarRef.current) {
        sidebarRef.current.scrollTop = sidebarScrollRef.current;
        console.log(
          "[RESTORE] Sidebar scroll restored to:",
          sidebarScrollRef.current
        );
      }

      // Prevent window from scrolling to top - maintain current position
      if (Math.abs(window.scrollY - currentWindowScroll) > 10) {
        window.scrollTo({ top: currentWindowScroll, behavior: "instant" });
        console.log(
          "[RESTORE] Window scroll maintained at:",
          currentWindowScroll
        );
      }
    };

    // Use requestAnimationFrame to ensure DOM is ready
    requestAnimationFrame(() => {
      setTimeout(restoreScroll, 100);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [document]); // Only depend on document, not items.length to avoid conflicts

  const handleRefine = async () => {
    if (!selectedItem || !refinementPrompt.trim()) {
      setError("Please select an item and enter a refinement prompt");
      return;
    }

    // CRITICAL: Lock the selected item ID BEFORE any async operations
    const selectedItemId = selectedItem.id;
    const selectedItemTitle = selectedItem.title;

    console.log("[REFINE_START] ============================================");
    console.log("[REFINE_START] 1. BEFORE REFINE CLICK:");
    console.log("[REFINE_START]   selectedItem:", {
      id: selectedItem.id,
      title: selectedItem.title,
    });
    console.log(
      "[REFINE_START]   selectedItemIdRef:",
      selectedItemIdRef.current
    );
    console.log("[REFINE_START]   isInitialized:", isInitializedRef.current);
    console.log("[REFINE_START] ============================================");

    // Set refining flag to prevent selection reset
    isRefiningRef.current = true;
    selectedItemIdRef.current = selectedItemId;

    console.log("[REFINE_START] Section ID:", selectedItemId);
    console.log("[REFINE_START] Section Title:", selectedItemTitle);
    console.log("[REFINE_START] Prompt:", refinementPrompt);
    console.log(
      "[REFINE_START] Current content:",
      content[selectedItemId]?.substring(0, 100) + "..."
    );
    console.log(
      "[REFINE_START] Locked selectedItemIdRef to:",
      selectedItemIdRef.current
    );

    setLoading(true);
    setError("");
    // Don't clear success state here - keep it for other features (feedback/comments)
    // Success message removed for refinement to keep UI clean and distraction-free

    try {
      const response = await refinementAPI.refineContent(
        project.id,
        selectedItemId,
        refinementPrompt
      );

      // Handle response - Axios wraps the response in .data
      const refinementData = response.data;

      if (!refinementData || !refinementData.new_content) {
        throw new Error("Invalid response from server: missing new_content");
      }

      console.log(
        "[REFINE_SUCCESS] ============================================"
      );
      console.log("[REFINE_SUCCESS] 2. IMMEDIATELY AFTER REFINE API RESPONSE:");
      console.log("[REFINE_SUCCESS]   selectedItem:", {
        id: selectedItem?.id,
        title: selectedItem?.title,
      });
      console.log(
        "[REFINE_SUCCESS]   selectedItemIdRef:",
        selectedItemIdRef.current
      );
      console.log(
        "[REFINE_SUCCESS]   Response section_id:",
        refinementData.section_id
      );
      console.log(
        "[REFINE_SUCCESS]   New content length:",
        refinementData.new_content?.length || 0
      );
      console.log(
        "[REFINE_SUCCESS] ============================================"
      );

      // Scroll positions were already saved at the start of handleRefine
      // Just verify they're still correct
      console.log("[REFINE_SUCCESS] Current scroll positions:", {
        content: scrollPositionRef.current,
        sidebar: sidebarScrollRef.current,
      });

      // Update local content state IMMEDIATELY - this ensures UI updates right away
      setContent((prev) => {
        const updated = {
          ...prev,
          [selectedItemId]: refinementData.new_content,
        };
        console.log(
          "[REFINE_SUCCESS] Local content updated. All section IDs:",
          Object.keys(updated)
        );
        return updated;
      });

      // CRITICAL: Reset feedback state for this section after refinement
      // New content requires fresh feedback - old reactions don't apply
      setSectionFeedback((prev) => {
        const updated = { ...prev };
        updated[selectedItemId] = null; // Clear feedback for this section
        console.log(
          "[REFINE_SUCCESS] Feedback reset for section:",
          selectedItemId
        );
        return updated;
      });

      // Success message removed for clean, distraction-free UI
      setRefinementPrompt("");

      // Refresh document from server to get latest content
      // The useEffect watching [document] will restore selection and scroll automatically
      if (onUpdate) {
        console.log("[REFINE_SUCCESS] Refreshing document from server...");
        console.log("[REFINE_SUCCESS] BEFORE onUpdate - selectedItem:", {
          id: selectedItem?.id,
          title: selectedItem?.title,
        });
        console.log(
          "[REFINE_SUCCESS] BEFORE onUpdate - selectedItemIdRef:",
          selectedItemIdRef.current
        );

        await onUpdate();

        console.log("[REFINE_SUCCESS] AFTER onUpdate - selectedItem:", {
          id: selectedItem?.id,
          title: selectedItem?.title,
        });
        console.log(
          "[REFINE_SUCCESS] AFTER onUpdate - selectedItemIdRef:",
          selectedItemIdRef.current
        );
        console.log("[REFINE_SUCCESS] Document refreshed");

        // Verify the updated content is in the document
        // Note: This will be checked after the useEffect runs
        setTimeout(() => {
          console.log("[REFINE_SUCCESS] Verifying updated content...");
          console.log(
            "[REFINE_SUCCESS] Current document content keys:",
            Object.keys(document?.content || {})
          );
          console.log(
            "[REFINE_SUCCESS] Content for selected section:",
            document?.content?.[selectedItemId]?.substring(0, 100) ||
              "NOT FOUND"
          );
        }, 300);
      }

      // Clear refining flag after a short delay to allow useEffect to run
      // Also ensure selection is explicitly restored
      setTimeout(() => {
        console.log(
          "[REFINE_COMPLETE] ============================================"
        );
        console.log("[REFINE_COMPLETE] 3. AFTER DOCUMENT REFRESH:");
        console.log("[REFINE_COMPLETE]   selectedItem:", {
          id: selectedItem?.id,
          title: selectedItem?.title,
        });
        console.log(
          "[REFINE_COMPLETE]   selectedItemIdRef:",
          selectedItemIdRef.current
        );
        console.log("[REFINE_COMPLETE]   isRefining:", isRefiningRef.current);
        console.log(
          "[REFINE_COMPLETE] ============================================"
        );

        isRefiningRef.current = false;
        console.log(
          "[REFINE_COMPLETE] Cleared isRefiningRef, restoring selection..."
        );

        // Explicitly restore selection after clearing the flag
        // CRITICAL FIX: Only update if selectedItem is NULL or doesn't match
        if (selectedItemIdRef.current && items.length > 0) {
          const matchingItem = items.find(
            (item) => item.id === selectedItemIdRef.current
          );
          if (matchingItem) {
            // CRITICAL FIX: Check if selectedItem already matches - if so, DO NOT overwrite
            if (
              selectedItem !== null &&
              selectedItem.id === selectedItemIdRef.current
            ) {
              console.log(
                "[REFINE_COMPLETE] ✅ selectedItem already matches ref, DO NOT overwrite:",
                {
                  id: selectedItem.id,
                  title: selectedItem.title,
                }
              );
              // Selection is already correct, just restore scroll
              requestAnimationFrame(() => {
                if (contentDisplayRef.current) {
                  contentDisplayRef.current.scrollTop =
                    scrollPositionRef.current;
                } else if (refinementContentRef.current) {
                  refinementContentRef.current.scrollTop =
                    scrollPositionRef.current;
                }
                if (sidebarRef.current) {
                  sidebarRef.current.scrollTop = sidebarScrollRef.current;
                }
              });
            } else {
              console.log("[REFINE_COMPLETE] ✅ Updating selection because:", {
                selectedItemIsNull: selectedItem === null,
                reason:
                  selectedItem === null
                    ? "selectedItem is NULL"
                    : "selectedItem does not match ref",
              });
              console.log("[REFINE_COMPLETE]   Restoring to:", {
                id: matchingItem.id,
                title: matchingItem.title,
              });
              setSelectedItem(matchingItem);

              // Restore scroll positions after selection is restored
              requestAnimationFrame(() => {
                setTimeout(() => {
                  // Restore main content scroll
                  if (contentDisplayRef.current) {
                    contentDisplayRef.current.scrollTop =
                      scrollPositionRef.current;
                  } else if (refinementContentRef.current) {
                    refinementContentRef.current.scrollTop =
                      scrollPositionRef.current;
                  }

                  // Restore sidebar scroll
                  if (sidebarRef.current) {
                    sidebarRef.current.scrollTop = sidebarScrollRef.current;
                  }

                  // Prevent window from scrolling - maintain current position
                  const currentWindowScroll = window.scrollY;
                  if (currentWindowScroll > 0) {
                    // Only restore if we were scrolled, otherwise stay at top
                    window.scrollTo({
                      top: currentWindowScroll,
                      behavior: "instant",
                    });
                  }

                  console.log("[REFINE_COMPLETE] Scroll positions restored:", {
                    content: scrollPositionRef.current,
                    sidebar: sidebarScrollRef.current,
                    window: currentWindowScroll,
                  });
                }, 50);
              });
            }
          } else {
            console.warn(
              "[REFINE_COMPLETE] ⚠️ Cannot restore - item not found:",
              selectedItemIdRef.current
            );
          }
        }

        console.log("[REFINE_COMPLETE] 4. AFTER ALL useEffect EXECUTIONS:");
        console.log("[REFINE_COMPLETE]   selectedItem:", {
          id: selectedItem?.id,
          title: selectedItem?.title,
        });
        console.log(
          "[REFINE_COMPLETE]   selectedItemIdRef:",
          selectedItemIdRef.current
        );
        console.log(
          "[REFINE_COMPLETE] Selection and scroll should be restored"
        );
        console.log(
          "[REFINE_COMPLETE] ============================================"
        );
      }, 300);
    } catch (err) {
      isRefiningRef.current = false;
      console.error(
        "[REFINE_ERROR] ============================================"
      );
      console.error("[REFINE_ERROR] Refinement failed:", err);
      console.error(
        "[REFINE_ERROR] ============================================"
      );
      const errorMsg =
        err.extractedMessage ||
        err.response?.data?.detail ||
        err.message ||
        "Failed to refine content";
      setError(
        typeof errorMsg === "string" ? errorMsg : "Failed to refine content"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (sectionId, feedbackType) => {
    if (!sectionId) {
      return;
    }

    // Toggle: if clicking the same button, unselect it
    const currentFeedback = sectionFeedback[sectionId];
    const newFeedback = currentFeedback === feedbackType ? null : feedbackType;

    // Optimistically update UI immediately
    setSectionFeedback((prev) => ({
      ...prev,
      [sectionId]: newFeedback,
    }));

    try {
      // Send feedback to backend (null to reset, or like/dislike)
      // Backend handles: UPDATE existing row or DELETE if null
      await refinementAPI.submitFeedback(project.id, sectionId, newFeedback);
      console.log("[FEEDBACK] Feedback updated:", {
        sectionId,
        previous: currentFeedback,
        new: newFeedback,
      });
    } catch (err) {
      // Revert on error
      setSectionFeedback((prev) => ({
        ...prev,
        [sectionId]: currentFeedback, // Revert to previous state
      }));

      const errorMsg =
        err.extractedMessage ||
        err.response?.data?.detail ||
        err.message ||
        "Failed to submit feedback";
      console.error("[FEEDBACK] Error:", errorMsg);
      // Don't show error to user - keep UI clean
    }
  };

  const handleAddComments = async () => {
    if (!selectedItem || !comments.trim()) {
      setError("Please select an item and enter comments");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      await refinementAPI.addComments(project.id, selectedItem.id, comments);
      setSuccess("Comments added.");
      setComments("");
    } catch (err) {
      const errorMsg =
        err.extractedMessage ||
        err.response?.data?.detail ||
        err.message ||
        "Failed to add comments";
      setError(
        typeof errorMsg === "string" ? errorMsg : "Failed to add comments"
      );
    } finally {
      setLoading(false);
    }
  };

  if (!document || !content) {
    return (
      <div className="info-message">
        Please generate content first before refining.
      </div>
    );
  }

  return (
    <div className="refinement-interface">
      <h2>Refine Content</h2>

      <div className="refinement-layout">
        <div className="items-sidebar" ref={sidebarRef}>
          <h3>Select {itemType.charAt(0).toUpperCase() + itemType.slice(1)}</h3>
          {items.map((item) => (
            <div
              key={item.id}
              className={`item-selector ${
                selectedItem?.id === item.id ? "active" : ""
              }`}
              onClick={(e) => {
                console.log(
                  "[USER_CLICK] User clicked section:",
                  item.id,
                  item.title
                );
                console.log("[USER_CLICK] BEFORE click - selectedItem:", {
                  id: selectedItem?.id,
                  title: selectedItem?.title,
                });
                console.log(
                  "[USER_CLICK] BEFORE click - selectedItemIdRef:",
                  selectedItemIdRef.current
                );

                // Save scroll positions BEFORE any state changes
                if (contentDisplayRef.current) {
                  scrollPositionRef.current =
                    contentDisplayRef.current.scrollTop;
                }
                if (sidebarRef.current) {
                  sidebarScrollRef.current = sidebarRef.current.scrollTop;
                }
                const currentWindowScroll = window.scrollY;

                // Prevent any default scroll behavior
                e.preventDefault();
                e.stopPropagation();

                // Update both ref and state immediately
                selectedItemIdRef.current = item.id;
                setSelectedItem(item);
                // Mark as initialized to prevent auto-selection
                isInitializedRef.current = true;

                console.log("[USER_CLICK] AFTER click - selectedItem:", {
                  id: item.id,
                  title: item.title,
                });
                console.log(
                  "[USER_CLICK] AFTER click - selectedItemIdRef:",
                  selectedItemIdRef.current
                );

                // Prevent any scroll jumps after selection change
                requestAnimationFrame(() => {
                  // Restore scroll positions to prevent jumps
                  if (contentDisplayRef.current) {
                    contentDisplayRef.current.scrollTop =
                      scrollPositionRef.current;
                  }
                  if (sidebarRef.current) {
                    sidebarRef.current.scrollTop = sidebarScrollRef.current;
                  }
                  if (currentWindowScroll > 0) {
                    window.scrollTo({
                      top: currentWindowScroll,
                      behavior: "instant",
                    });
                  }
                });
              }}
            >
              {item.title}
            </div>
          ))}
        </div>

        <div className="refinement-content" ref={refinementContentRef}>
          {selectedItem ? (
            <>
              {/* Unified Content Block - Content + Feedback as One Entity */}
              <div className="content-block" ref={contentDisplayRef}>
                {/* Section Title */}
                <div className="content-block-header">
                  <h3>
                    {selectedItem.title}
                    {process.env.NODE_ENV === "development" && (
                      <span
                        style={{
                          fontSize: "0.7em",
                          color: "var(--text-tertiary)",
                          fontWeight: "normal",
                          marginLeft: "8px",
                        }}
                      >
                        (ID: {selectedItem.id})
                      </span>
                    )}
                  </h3>
                </div>

                {/* Content Divider */}
                <div className="content-divider"></div>

                {/* Generated/Refined Content */}
                <div className="content-block-body">
                  {content[selectedItem.id] ? (
                    <div className="content-text">
                      <pre>{content[selectedItem.id]}</pre>
                    </div>
                  ) : (
                    <p className="no-content">No content available</p>
                  )}
                </div>

                {/* Content Divider */}
                {content[selectedItem.id] && (
                  <div className="content-divider"></div>
                )}

                {/* Feedback Actions - Visually Tied to Content */}
                {content[selectedItem.id] && (
                  <div className="content-block-actions">
                    <button
                      className={`feedback-button feedback-like ${
                        sectionFeedback[selectedItem.id] === "like"
                          ? "active"
                          : ""
                      }`}
                      onClick={() => handleFeedback(selectedItem.id, "like")}
                      aria-label="Like this section"
                    >
                      <span className="feedback-icon">👍</span>
                      <span className="feedback-label">Like</span>
                    </button>
                    <button
                      className={`feedback-button feedback-dislike ${
                        sectionFeedback[selectedItem.id] === "dislike"
                          ? "active"
                          : ""
                      }`}
                      onClick={() => handleFeedback(selectedItem.id, "dislike")}
                      aria-label="Dislike this section"
                    >
                      <span className="feedback-icon">👎</span>
                      <span className="feedback-label">Dislike</span>
                    </button>
                  </div>
                )}
              </div>

              <div className="refinement-actions">
                <div className="refinement-section">
                  <h4>AI Refinement</h4>
                  <textarea
                    value={refinementPrompt}
                    onChange={(e) => setRefinementPrompt(e.target.value)}
                    placeholder="Enter refinement prompt (e.g., 'Make this more formal', 'Convert to bullet points')"
                    rows="3"
                  />
                  <button
                    className="btn btn-primary"
                    onClick={handleRefine}
                    disabled={loading || !refinementPrompt.trim()}
                  >
                    {loading ? "Refining" : "Refine"}
                  </button>
                </div>

                <div className="refinement-section">
                  <h4>Comments</h4>
                  <textarea
                    value={comments}
                    onChange={(e) => setComments(e.target.value)}
                    placeholder="Add your comments..."
                    rows="3"
                  />
                  <button
                    className="btn btn-secondary"
                    onClick={handleAddComments}
                    disabled={loading || !comments.trim()}
                  >
                    Add Comments
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="info-message">
              Select a {itemType} from the sidebar to refine
            </div>
          )}
        </div>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}
    </div>
  );
};

export default RefinementInterface;
