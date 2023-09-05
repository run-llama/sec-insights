import React from "react";

// https://gist.github.com/carpben/de968e377cbac0ffbdefe1ab56237573
export default function useFocus<T extends HTMLElement = HTMLElement>() {
  const ref = React.useRef<T>(null);
  const setFocus = () => ref?.current?.focus?.();

  return [ref, setFocus] as const;
}
