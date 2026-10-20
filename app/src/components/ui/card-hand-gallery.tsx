"use client";

import * as React from "react";
import { motion, useReducedMotion } from "motion/react";
import { cn } from "@/lib/utils";

export interface FanCardItem {
  /** Stable, unique identifier. */
  id: string;
  /** Image URL rendered as the card face. */
  src: string;
  /** Shown beside the fan while this card is active, and its accessible name. */
  title: string;
  /** Shown on the opposite side while this card is active. */
  description?: string;
  /** Optional custom fit for architecture diagrams vs photos */
  fit?: "cover" | "contain";
}

export interface CardHandGalleryProps {
  /** Cards in the hand, in fan order. */
  cards: readonly FanCardItem[];
  /** Active card id. Pass to control the selection yourself. */
  activeId?: string;
  /** Card width in pixels. Height follows a 5:7 ratio. Shrinks to fit narrow containers. */
  cardWidth?: number;
  className?: string;
  /** Initially active card. Defaults to the first card. */
  defaultActiveId?: string;
  /** Fires when a different card is picked. */
  onSelect?: (card: FanCardItem) => void;
}

/** Flick speed, in px/s, that selects a card regardless of how far it travelled. */
const SELECT_VELOCITY = -600;

/** Cards waiting in the hand sit behind the active one, so they ride smaller. */
const HAND_SCALE = 0.85;

/** Spread each card into a symmetric arc around the middle of the hand. */
function fanTransform(index: number, count: number, spacing: number) {
  const offset = index - (count - 1) / 2;
  // Subtle rotation for landscape cards so text/charts stay clear and readable
  const stepDeg = count > 1 ? Math.min(4.5, 24 / (count - 1)) : 0;
  const rotate = offset * stepDeg;

  return {
    rotate,
    x: offset * spacing,
    y: Math.abs(rotate) * 2.2,
  };
}

export function CardHandGallery({
  cards,
  activeId: controlledActiveId,
  cardWidth = 740,
  className,
  defaultActiveId,
  onSelect,
}: CardHandGalleryProps) {
  const shouldReduceMotion = useReducedMotion();
  const fanRef = React.useRef<HTMLDivElement>(null);
  // Set while a pointer drag is in flight so the trailing click is ignored.
  const draggingRef = React.useRef(false);
  const [fanWidth, setFanWidth] = React.useState<number | null>(null);
  const [internalActiveId, setInternalActiveId] = React.useState(
    defaultActiveId ?? cards[0]?.id,
  );
  const [hoveredId, setHoveredId] = React.useState<string | null>(null);
  // Dragging a card claims the vertical touch axis, which on a phone means
  // swiping over the fan scrolls nothing. Pointer devices only.
  const [canDrag, setCanDrag] = React.useState(false);

  // Fall back to the first card whenever the requested id is not in the hand:
  // a swapped `cards` array, a stale controlled id, a bad `defaultActiveId`.
  // Without this the fan has no card lifted and no side text — an empty state
  // that is otherwise unreachable.
  const requestedId = controlledActiveId ?? internalActiveId;
  const activeId = cards.some((card) => card.id === requestedId)
    ? requestedId
    : cards[0]?.id;
  const activeIndex = cards.findIndex((card) => card.id === activeId);
  const activeCard = cards[activeIndex];

  React.useEffect(() => {
    setCanDrag(!window.matchMedia("(pointer: coarse)").matches);
  }, []);

  React.useEffect(() => {
    const node = fanRef.current;

    if (!node) {
      return;
    }

    const observer = new ResizeObserver(([entry]) => {
      setFanWidth(entry.contentRect.width);
    });

    observer.observe(node);

    return () => observer.disconnect();
  }, []);

  // Cards scale generously on wide viewports matching the dashboard image
  const width =
    fanWidth === null
      ? cardWidth
      : Math.min(cardWidth, Math.max(320, fanWidth * 0.94));

  // Exact 16:9 aspect ratio matching page_1_executive_operations.png (1702x954)
  const height = Math.round(width / (16 / 9));
  const baseBottom = Math.round(height * 0.08);
  const hoverLift = Math.round(height * 0.22);
  const activeLift = Math.round(height * 0.38);
  const selectDistance = -Math.round(height * 0.45);

  const handCards = cards.filter((card) => card.id !== activeId);
  const hoveredIndex = hoveredId
    ? handCards.findIndex((card) => card.id === hoveredId)
    : -1;

  // Clamp the horizontal spread so the outermost cards never clip against column edges
  const maxOffset = (handCards.length - 1) / 2;
  const halfAvailable =
    fanWidth === null ? Number.POSITIVE_INFINITY : fanWidth / 2 - width * 0.44;
  const fanSpacing =
    maxOffset > 0
      ? Math.min(
          width * (handCards.length > 5 ? 0.16 : 0.22),
          Math.max(width * 0.08, halfAvailable / maxOffset),
        )
      : 0;

  const cardTransition = shouldReduceMotion
    ? { duration: 0.16, ease: "easeOut" as const }
    : {
        damping: 30,
        mass: 0.9,
        stiffness: 340,
        type: "spring" as const,
      };

  const textTransition = { duration: shouldReduceMotion ? 0 : 0.32 };
  const textOffset = shouldReduceMotion ? 0 : 10;

  function clearHover(id: string) {
    setHoveredId((current) => (current === id ? null : current));
  }

  function selectCard(card: FanCardItem) {
    if (card.id === activeId) {
      return;
    }

    clearHover(card.id);

    if (controlledActiveId === undefined) {
      setInternalActiveId(card.id);
    }

    onSelect?.(card);
  }

  return (
    <div className={cn("flex flex-col items-center w-full", className)}>
      {/* Main 3-Column Showcase Layout */}
      <div className="flex w-full flex-col items-center gap-8 lg:flex-row lg:items-center lg:gap-8 xl:gap-12 2xl:gap-16">
        {/* Left Column: Scaled Accent Headline ("Numbers are useful...") */}
        <div className="relative z-20 w-full shrink-0 text-center lg:w-72 xl:w-80 2xl:w-[360px] lg:text-right">
          {activeCard ? (
            <motion.div
              animate={{ opacity: 1, y: 0 }}
              initial={{ opacity: 0, y: textOffset }}
              key={activeCard.id}
              transition={textTransition}
            >
              <p className="font-mono text-xs sm:text-sm lg:text-base tabular-nums text-[#DDA15E] font-semibold tracking-widest uppercase">
                STAGE {String(activeIndex + 1).padStart(2, "0")} /{" "}
                {String(cards.length).padStart(2, "0")}
              </p>
              <h3 className="mt-3 sm:mt-4 text-balance font-extrabold text-2xl sm:text-3xl lg:text-[2.2rem] xl:text-[2.75rem] 2xl:text-[3.15rem] text-[#FEFAE0] leading-[1.12] tracking-tight">
                {activeCard.title}
              </h3>
            </motion.div>
          ) : null}
        </div>

        {/* Center Showcase: Flush 16:9 Device Mockup Fan & Stack */}
        <div
          className="relative w-full min-w-0 flex-1 flex justify-center"
          ref={fanRef}
          style={{ minHeight: Math.round(height * 1.54) }}
        >
          {cards.map((card) => {
            const isActive = card.id === activeId;
            const handIndex = handCards.findIndex(
              (candidate) => candidate.id === card.id,
            );

            let slot: { rotate: number; scale: number; x: number; y: number };
            let lift = { rotate: 0, scale: 1, x: 0, y: 0 };
            let zIndex: number;

            if (isActive) {
              slot = { rotate: 0, scale: 1, x: 0, y: -activeLift };
              zIndex = 100;
            } else {
              const fan = fanTransform(handIndex, handCards.length, fanSpacing);
              const isHovered = card.id === hoveredId;
              const neighborShift =
                hoveredIndex !== -1 && !isHovered
                  ? (Math.sign(handIndex - hoveredIndex) * width * 0.12) /
                    Math.max(1, Math.abs(handIndex - hoveredIndex))
                  : 0;
              const dx = neighborShift;
              const dy = isHovered ? -hoverLift - fan.y : 0;
              const rad = (-fan.rotate * Math.PI) / 180;

              slot = {
                rotate: fan.rotate,
                scale: HAND_SCALE,
                x: fan.x,
                y: fan.y,
              };
              lift = {
                rotate: isHovered ? -fan.rotate * 0.45 : 0,
                scale: isHovered ? 1.06 : 1,
                x: (dx * Math.cos(rad) - dy * Math.sin(rad)) / HAND_SCALE,
                y: (dx * Math.sin(rad) + dy * Math.cos(rad)) / HAND_SCALE,
              };
              zIndex = isHovered ? 60 : 10 + handIndex;
            }

            return (
              <motion.div
                animate={slot}
                className="absolute left-1/2"
                initial={false}
                key={card.id}
                onHoverEnd={() => clearHover(card.id)}
                onHoverStart={() => {
                  if (!isActive) {
                    setHoveredId(card.id);
                  }
                }}
                style={{ bottom: baseBottom, marginLeft: -width / 2, zIndex }}
                transition={cardTransition}
              >
                <motion.div
                  animate={lift}
                  initial={false}
                  transition={cardTransition}
                >
                  <motion.button
                    aria-label={card.title}
                    aria-pressed={isActive}
                    className={cn(
                      "block rounded-2xl sm:rounded-3xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#BC6C25] focus-visible:ring-offset-2 focus-visible:ring-offset-[#0A0F08] transition-all duration-300",
                      isActive
                        ? "cursor-default"
                        : "cursor-grab active:cursor-grabbing",
                    )}
                    drag={canDrag && !isActive ? "y" : false}
                    dragConstraints={{ bottom: 0, top: -height * 1.4 }}
                    dragElastic={0.12}
                    dragSnapToOrigin
                    onBlur={() => clearHover(card.id)}
                    onClick={() => {
                      if (draggingRef.current) {
                        draggingRef.current = false;
                        return;
                      }

                      selectCard(card);
                    }}
                    onDragEnd={(_event, info) => {
                      if (
                        info.offset.y < selectDistance ||
                        info.velocity.y < SELECT_VELOCITY
                      ) {
                        selectCard(card);
                      }
                    }}
                    onDragStart={() => {
                      draggingRef.current = true;
                    }}
                    onFocus={() => {
                      if (!isActive) {
                        setHoveredId(card.id);
                      }
                    }}
                    onPointerDown={() => {
                      draggingRef.current = false;
                    }}
                    type="button"
                  >
                    {/* Modern Flush Device Mockup Frame tightly matching 16:9 Image Geometry */}
                    <div
                      className={cn(
                        "relative overflow-hidden rounded-2xl sm:rounded-3xl border transition-all duration-300 shadow-2xl aspect-[16/9] flex items-center justify-center bg-[#10170D]",
                        isActive
                          ? "border-[#BC6C25]/70 shadow-[0_25px_60px_-10px_rgba(0,0,0,0.9),0_0_0_1px_rgba(188,108,37,0.45)] ring-1 ring-[#BC6C25]/50"
                          : "border-[#606C38]/35 bg-[#141C0D] shadow-[0_15px_35px_rgba(0,0,0,0.7)] hover:border-[#606C38]/60 hover:shadow-2xl",
                      )}
                      style={{ width, height }}
                    >
                      {/* Flush Screen Canvas */}
                      <img
                        alt={card.title}
                        className={cn(
                          "card-mockup-img select-none transition-transform duration-300",
                          card.fit === "contain"
                            ? "object-contain p-2 sm:p-3"
                            : "object-cover",
                        )}
                        draggable={false}
                        src={card.src}
                        style={{
                          width: "100%",
                          height: "100%",
                          maxHeight: "100%",
                          display: "block",
                          imageRendering: "auto",
                        }}
                      />

                      {/* Subtle Glass Surface Reflection / Precision Rim Highlight */}
                      <div className="absolute inset-0 pointer-events-none rounded-2xl sm:rounded-3xl ring-1 ring-inset ring-white/10" />
                    </div>
                  </motion.button>
                </motion.div>
              </motion.div>
            );
          })}
        </div>

        {/* Right Column: Scaled Narrative Body Paragraph */}
        <div
          aria-live="polite"
          className="relative z-20 w-full shrink-0 text-center lg:w-72 xl:w-80 2xl:w-[360px] lg:text-left"
        >
          {activeCard?.description ? (
            <motion.p
              animate={{ opacity: 1, y: 0 }}
              className="text-pretty text-base sm:text-lg lg:text-xl xl:text-[1.25rem] 2xl:text-[1.35rem] text-[#FEFAE0]/90 leading-[1.7] font-normal"
              initial={{ opacity: 0, y: textOffset }}
              key={activeCard.id}
              transition={textTransition}
            >
              {activeCard.description}
            </motion.p>
          ) : null}
        </div>
      </div>

      {/* Interactive Quick-Select Stage Pills (Dots Removed) */}
      <div className="flex items-center justify-center flex-wrap gap-2 sm:gap-3 mt-8 z-20">
        {cards.map((card, idx) => {
          const isActive = card.id === activeId;
          return (
            <button
              key={card.id}
              onClick={() => selectCard(card)}
              className={cn(
                "group flex items-center justify-center px-3.5 sm:px-4 py-1.5 rounded-full text-xs sm:text-sm font-mono transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#BC6C25]",
                isActive
                  ? "bg-[#BC6C25]/25 border border-[#BC6C25] text-[#FEFAE0] shadow-[0_0_14px_rgba(188,108,37,0.3)] font-semibold"
                  : "bg-[#283618]/50 border border-[#606C38]/30 text-[#FEFAE0]/75 hover:text-[#FEFAE0] hover:bg-[#283618]/80 hover:border-[#606C38]/60",
              )}
              title={card.title}
              type="button"
            >
              <span className="hidden sm:inline">Stage 0{idx + 1}</span>
              <span className="sm:hidden">0{idx + 1}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
