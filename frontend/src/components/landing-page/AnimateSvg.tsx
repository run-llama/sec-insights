import React, { useEffect, useState } from "react";

interface ScrollSVGProps {
  breakpoint: number;
  increment: number;
  svgs: JSX.Element[];
}

export const AnimateSvg: React.FC<ScrollSVGProps> = ({
  breakpoint,
  increment,
  svgs,
}) => {
  const [scrollPosition, setScrollPosition] = useState(0);

  // Listen to scroll event
  useEffect(() => {
    const handleScroll = () => {
      const currentScrollPos = window.pageYOffset;
      if (currentScrollPos > breakpoint) {
        setScrollPosition(
          Math.floor((currentScrollPos - breakpoint) / increment)
        );
      }
    };

    window.addEventListener("scroll", handleScroll);

    // Clean up event listener
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [breakpoint, increment]);

  // Function to render SVGs
  const renderSVG = () => {
    // If we've scrolled past all SVGs, keep showing the last one
    if (scrollPosition >= svgs.length) {
      return svgs[svgs.length - 1];
    }

    // Otherwise, show the SVG for the current scroll position
    return svgs[scrollPosition];
  };

  return <div>{renderSVG()}</div>;
};

export default AnimateSvg;
