import React from "react";
import ModalPortal from "./ModalPortal";
import { AiOutlineClose } from "react-icons/ai";
interface ModalProps {
  isOpen: boolean;
  toggleModal: () => void;
  title: string;
  children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({
  isOpen,
  toggleModal,
  title,
  children,
}) => {
  if (!isOpen) return null;

  return (
    <ModalPortal>
      <div className="fixed left-0 top-0 flex h-full w-full items-center justify-center">
        <div
          onClick={toggleModal}
          className="absolute h-full w-full bg-black opacity-50"
        ></div>
        <div className="relative z-10 max-w-[500px] rounded bg-white p-6 shadow-xl ">
          <h2 className="mb-2 text-xl font-bold">{title}</h2>
          {children}
          <button
            onClick={toggleModal}
            className="b absolute right-2 top-2 inline-flex h-7 w-7 items-center justify-center rounded-full p-1 text-base font-medium text-gray-90 hover:bg-gray-15 "
          >
            <AiOutlineClose size={24} />
          </button>
        </div>
      </div>
    </ModalPortal>
  );
};

export default Modal;
