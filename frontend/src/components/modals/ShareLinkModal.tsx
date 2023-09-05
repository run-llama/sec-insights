import React, { useRef, useEffect } from "react";
import Modal from "../basics/Modal";

interface ShareLinkModalProps {
  isOpen: boolean;
  toggleModal: () => void;
}

const ShareLinkModal: React.FC<ShareLinkModalProps> = ({
  isOpen,
  toggleModal,
}) => {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const copyToClipboard = (e: React.MouseEvent) => {
    e.preventDefault();
    inputRef.current?.select();
    document.execCommand("copy");
  };

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.select();
    }
  }, [isOpen]);

  return (
    <Modal isOpen={isOpen} toggleModal={toggleModal} title="Share Conversation">
      <p className="mb-6 mt-2 text-sm text-gray-500">
        Note: this is a public page. Anyone with this link can view the
        contents of the page. This statement is for informational purposes only
        and does not serve as professional financial advice.
      </p>

      <div className="flex items-center space-x-2">
        <input
          ref={inputRef}
          className="text-grey-darkest w-full border px-3 py-2"
          type="text"
          value={typeof window !== "undefined" ? window.location.href : ""}
          readOnly
        />
        <button
          onClick={copyToClipboard}
          className="rounded bg-llama-indigo px-4 py-2 font-bold text-white opacity-90 hover:opacity-100"
        >
          Copy
        </button>
      </div>
    </Modal>
  );
};

export default ShareLinkModal;
