import React from "react";
import ReactDOM from "react-dom";

interface ModalPortalProps {
  children: React.ReactNode;
}

const ModalPortal = ({ children }: ModalPortalProps) => {
  const domNode = document.getElementById("modal-root");
  return domNode ? ReactDOM.createPortal(children, domNode) : null;
};

export default ModalPortal;
