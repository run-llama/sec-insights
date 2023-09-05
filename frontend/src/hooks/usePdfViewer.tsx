// usePDFViewer.ts
import { useState, useEffect, useCallback } from "react";
import { usePdfFocus } from "~/context/pdf";

import type { PdfFocusHandler as PdfFocusHandler } from "~/components/pdf-viewer/VirtualizedPdf";
import React from "react";
import { SecDocument } from "~/types/document";

export const zoomLevels = [
  "50%",
  "80%",
  "100%",
  "130%",
  "200%",
  "300%",
  "400%",
];
const startZoomLevelIdx = 2;

const usePDFViewer = (file: SecDocument) => {
  const [scrolledIndex, setScrolledIndex] = useState(1);
  const [scale, setScale] = useState(1.0);
  const [scaleFit, setScaleFit] = useState(1.0);
  const [numPages, setNumPages] = useState(0);
  const [isPdfRendered, setIsPdfRendered] = useState(false);
  const [zoomLevelIdx, setZoomLevelIdx] = useState(startZoomLevelIdx);

  const { pdfFocusState } = usePdfFocus();

  const pdfFocusRef = React.useRef<PdfFocusHandler | null>(null);

  const goToPage = (page: number) => {
    if (pdfFocusRef.current) {
      pdfFocusRef.current.scrollToPage(page);
    }
  };

  useEffect(() => {
    const activeDocumentId = pdfFocusState.documentId;
    if (activeDocumentId === file.id) {
      if (pdfFocusState.pageNumber) {
        goToPage(pdfFocusState.pageNumber - 1);
      }
    }
  }, [file, pdfFocusState]);

  const setCurrentPageNumber = useCallback((n: number) => {
    setScrolledIndex(n);
  }, []);

  const handleZoomIn = useCallback(() => {
    const nextLevel = zoomLevelIdx + 1;
    if (nextLevel >= zoomLevels.length) {
      return;
    }
    setZoomLevel(zoomLevels[nextLevel] || "100%");
  }, [zoomLevelIdx, scrolledIndex, pdfFocusRef]);

  const handleZoomOut = useCallback(() => {
    const nextLevel = zoomLevelIdx - 1;
    if (nextLevel < 0) {
      return;
    }
    setZoomLevel(zoomLevels[nextLevel] || "100%");
  }, [zoomLevelIdx, scrolledIndex, pdfFocusRef]);

  const nextPage = () => {
    goToPage(scrolledIndex + 1);
  };

  const prevPage = () => {
    goToPage(scrolledIndex - 1);
  };

  const toPercentPlusBase = (n: number) => {
    return `${100 + n * 100}%`;
  };

  const setZoomLevel = useCallback(
    (zoomLevel: string) => {
      const newZoomLevelIdx = zoomLevels.indexOf(zoomLevel);
      const newScale = percentToScale(zoomLevel) + scaleFit - 1;
      setScale(newScale);
      setTimeout(() => {
        goToPage(scrolledIndex);
      }, 30);
      setZoomLevelIdx(newZoomLevelIdx);
    },
    [scrolledIndex]
  );

  function percentToScale(percent: string): number {
    const number = parseInt(percent, 10);
    return number / 100;
  }

  const scaleDiff = Math.round((scale - scaleFit) * 10) / 10;
  const scaleText = toPercentPlusBase(scaleDiff);

  useEffect(() => {
    setScale(scaleFit);
  }, [scaleFit]);

  const zoomInEnabled = zoomLevelIdx < zoomLevels.length - 1;
  const zoomOutEnabled = zoomLevelIdx > 0;

  return {
    scrolledIndex,
    setCurrentPageNumber,
    scale,
    setScaleFit,
    numPages,
    setNumPages,
    handleZoomIn,
    handleZoomOut,
    nextPage,
    prevPage,
    scaleText,
    isPdfRendered,
    setIsPdfRendered,
    pdfFocusRef,
    goToPage,
    setZoomLevel,
    zoomInEnabled,
    zoomOutEnabled,
  };
};

export default usePDFViewer;
