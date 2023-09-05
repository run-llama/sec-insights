import * as React from "react";
const RightArrow = (
  props: React.JSX.IntrinsicAttributes & React.SVGProps<SVGSVGElement>
) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={17}
    height={19}
    className="text-brown-600 transition-colors duration-200 hover:text-black"
    {...props}
  >
    <path
      fill={props.fill}
      d="M15.75 8.21 2.175.905C1.035.29-.285 1.355.075 2.6l1.86 6.51c.075.27.075.54 0 .81l-1.86 6.51c-.36 1.245.96 2.31 2.1 1.695L15.75 10.82a1.47 1.47 0 0 0 0-2.58v-.03Z"
    />
  </svg>
);
export default RightArrow;
