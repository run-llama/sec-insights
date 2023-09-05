import { useWindowWidth } from "@wojtekmaj/react-hooks";
import { useEffect, useState } from "react";

export const MOBILE_BREAKPOINT = 768;
export default function useIsMobile() {
  const windowWidth = useWindowWidth();
  const [isMobile, setIsMobile] = useState(false);
  useEffect(() => {
    if ((windowWidth || 0) < MOBILE_BREAKPOINT) {
      setIsMobile(true);
    } else {
      setIsMobile(false);
    }
  }, [windowWidth]);

  return { isMobile };
}
