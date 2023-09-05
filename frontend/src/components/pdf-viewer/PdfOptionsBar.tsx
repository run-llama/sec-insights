// PDFOptionsBar.tsx
import { useEffect, useState } from "react";
import {
  HiMiniMagnifyingGlassMinus,
  HiMiniMagnifyingGlassPlus,
} from "react-icons/hi2";
import { PiCaretDownBold, PiCaretUpBold } from "react-icons/pi";
import { zoomLevels } from "~/hooks/usePdfViewer";
import { SecDocument } from "~/types/document";
import { borderColors } from "~/utils/colors";

interface PDFOptionsBarProps {
  file: SecDocument;
  scrolledIndex: number;
  numPages: number;
  scaleText: string;
  nextPage: () => void;
  prevPage: () => void;
  handleZoomIn: () => void;
  handleZoomOut: () => void;
  goToPage: (n: number) => void;
  setZoomLevel: (percent: string) => void;
  zoomInEnabled: boolean;
  zoomOutEnabled: boolean;
}

export const PDFOptionsBar: React.FC<PDFOptionsBarProps> = ({
  file,
  scrolledIndex,
  numPages,
  scaleText,
  nextPage,
  prevPage,
  handleZoomIn,
  handleZoomOut,
  goToPage,
  setZoomLevel,
  zoomInEnabled,
  zoomOutEnabled,
}) => {
  const [zoomPopoverOpen, setZoomPopoverOpen] = useState(false);

  const handleZoomSelection = (zoom: string) => {
    setZoomLevel(zoom);
    setZoomPopoverOpen(false);
  };

  const [inputValue, setInputValue] = useState(`${scrolledIndex + 1}`);

  useEffect(() => {
    setInputValue(`${scrolledIndex + 1}`);
  }, [scrolledIndex]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      const value = parseInt(inputValue, 10);
      if (!isNaN(value) && value > 0) {
        scrollToPage(value - 1);
      }
    }
  };

  const scrollToPage = (page: number) => {
    goToPage(page);
  };

  return (
    <div
      className={`flex h-[44px] w-full items-center justify-between border-b-2 `}
    >
      <div className="ml-3 flex w-1/2 items-center justify-start ">
        <div
          className={`flex items-center justify-center border-l-4 pl-2 ${
            borderColors[file.color]
          } `}
        >
          <div className="text font-bold">{file.ticker}</div>
          <div className="ml-2">
            {" "}
            {file.year} {file.quarter && `Q${file.quarter}`}
          </div>
        </div>
      </div>
      <div className="flex flex-grow items-center justify-center border-l border-l-gray-30">
        <div className="flex h-[30px] w-[350px] items-center justify-between">
          <div className="ml-4 flex w-[140px] text-gray-90">
            <button
              className="p-1 enabled:hover:rounded enabled:hover:bg-gray-15 disabled:text-gray-30 "
              onClick={prevPage}
              disabled={scrolledIndex === 0}
            >
              <PiCaretUpBold />
            </button>
            <div className="flex items-center justify-center">
              <input
                className="ml-1 h-[25px] w-[36px] rounded border py-2  pl-1 text-left focus:outline-none"
                value={inputValue}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
              />
            </div>
            <div className="ml-1 mt-[.5px]"> / {numPages}</div>
            <button
              className="ml-1 p-1 enabled:hover:rounded enabled:hover:bg-gray-15 disabled:text-gray-30 "
              onClick={nextPage}
              disabled={scrolledIndex === numPages - 1}
            >
              <PiCaretDownBold />
            </button>
          </div>
          <div className="mx-2 h-5/6 rounded border-l border-gray-30"></div>{" "}
          <div className="relative">
            <div className="mr-5 flex items-center justify-between ">
              <button
                className="mr-2 p-1 text-gray-90 enabled:hover:rounded enabled:hover:bg-gray-15 disabled:text-gray-60"
                onClick={handleZoomOut}
                disabled={!zoomOutEnabled}
              >
                <HiMiniMagnifyingGlassMinus size={22} />
              </button>
              <div
                className="w-[70px] cursor-pointer rounded px-1 px-2 hover:bg-gray-15 "
                onClick={() => setZoomPopoverOpen(!zoomPopoverOpen)}
              >
                <div className="flex items-center justify-center">
                  {scaleText}
                  {!zoomPopoverOpen ? (
                    <PiCaretDownBold size={16} />
                  ) : (
                    <PiCaretDownBold size={16} className="rotate-180" />
                  )}
                </div>
              </div>
              {zoomPopoverOpen && (
                <div className="absolute right-[55px] top-[30px] z-20 mb-2 rounded border bg-white py-1 text-black shadow">
                  {zoomLevels.map((zoom, index) => (
                    <button
                      key={index}
                      className="block w-full px-4 py-1 text-left text-sm hover:bg-gray-200"
                      onClick={() => handleZoomSelection(zoom)}
                    >
                      {zoom}
                    </button>
                  ))}
                </div>
              )}
              <button
                className="ml-2 p-1 text-gray-90 enabled:hover:rounded enabled:hover:bg-gray-15 disabled:text-gray-60 "
                onClick={handleZoomIn}
                disabled={!zoomInEnabled}
              >
                <HiMiniMagnifyingGlassPlus size={22} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
