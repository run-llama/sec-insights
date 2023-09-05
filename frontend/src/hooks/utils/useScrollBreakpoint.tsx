import { useRef, useEffect, useState } from "react";

export const useScrollBreakpoint = (offset = 0) => {
  const ref = useRef<HTMLDivElement>(null);
  const [breakpoint, setBreakpoint] = useState(0);

  useEffect(() => {
    const setTop = () => {
      if (ref.current) {
        const rect = ref.current.getBoundingClientRect();
        setBreakpoint(rect.top + window.scrollY - rect.height + offset);
      }
    };

    window.addEventListener("load", setTop);
    window.addEventListener("resize", setTop);

    return () => {
      window.removeEventListener("load", setTop);
      window.removeEventListener("resize", setTop);
    };
  }, []);

  return { ref, breakpoint };
};

export default useScrollBreakpoint;
