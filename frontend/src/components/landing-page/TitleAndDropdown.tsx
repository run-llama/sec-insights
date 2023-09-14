import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";

import { FiTrash2 } from "react-icons/fi";
import GitHubButton from "react-github-btn";

import cx from "classnames";
import type { SelectOption } from "~/types/selection";

import { DocumentSelectCombobox } from "~/components/landing-page/SelectTicker";
import Select from "react-select";
import {
  MAX_NUMBER_OF_SELECTED_DOCUMENTS,
  useDocumentSelector,
} from "~/hooks/useDocumentSelector";
import { backendClient } from "~/api/backend";
import { AiOutlineArrowRight, AiTwotoneCalendar } from "react-icons/ai";
import { CgFileDocument } from "react-icons/cg";
import { customReactSelectStyles } from "~/styles/react-select";
import { useIntercom } from "react-use-intercom";
import { LoadingSpinner } from "~/components/basics/Loading";
import useIsMobile from "~/hooks/utils/useIsMobile";

export const TitleAndDropdown = () => {
  const router = useRouter();

  const { isMobile } = useIsMobile();

  const [isLoadingConversation, setIsLoadingConversation] = useState(false);
  const handleSubmit = (event: { preventDefault: () => void }) => {
    setIsLoadingConversation(true);
    event.preventDefault();
    const selectedDocumentIds = selectedDocuments.map((val) => val.id);
    backendClient
      .createConversation(selectedDocumentIds)
      .then((newConversationId) => {
        setIsLoadingConversation(false);
        router
          .push(`/conversation/${newConversationId}`)
          .catch(() => console.log("error navigating to conversation"));
      })
      .catch(() => console.log("error creating conversation "));
  };

  const {
    availableTickers,
    availableDocumentTypes,
    sortedAvailableYears,
    selectedDocuments,
    selectedTicker,
    selectedDocumentType,
    selectedYear,
    setSelectedYear,
    handleAddDocument,
    handleRemoveDocument,
    isDocumentSelectionEnabled,
    isStartConversationButtonEnabled,
    yearFocusRef,
    documentTypeFocusRef,
    selectTicker,
    selectDocumentType,
    shouldFocusCompanySelect,
    setShouldFocusCompanySelect,
    sortedSelectedDocuments,
  } = useDocumentSelector();

  const { boot } = useIntercom();

  useEffect(() => {
    boot();
  }, []);

  return (
    <div className="landing-page-gradient-1 relative flex h-max w-screen flex-col items-center font-lora ">
      <div className="absolute right-4 top-4">
        <a href="https://www.llamaindex.ai/" target="_blank">
          <button className="flex items-center justify-center font-nunito text-lg font-bold ">
            Built by LlamaIndex
            <img src="logo-black.svg" className="mx-2 rounded-lg" width={40} />
          </button>
        </a>
      </div>
      <div className="mt-28 flex flex-col items-center">
        <div className="w-4/5 text-center text-4xl">
          Empower your organization&apos;s Business Intelligence with{" "}
          <span className="font-bold">SEC Insights </span>
        </div>
        <div className="mt-4 flex items-center justify-center">
          <div className="w-3/5 text-center font-nunito">
            Effortlessly analyze multifaceted financial documents such as 10-Ks
            and 10-Qs.
          </div>
        </div>
        <div className="mt-4 flex items-center justify-center">
          <GitHubButton href="https://github.com/run-llama/sec-insights">Open-Sourced on Github</GitHubButton>
        </div>
      </div>
      {isMobile ? (
        <div className="mt-12 flex h-1/5 w-11/12 rounded border p-4 text-center">
          <div className="text-xl font-bold">
            To start analyzing documents, please switch to a larger screen!
          </div>
        </div>
      ) : (
        <div className="mt-5 flex h-min w-11/12 max-w-[1200px] flex-col items-center justify-center rounded-lg border-2 bg-white sm:h-[400px] md:w-9/12 ">
          <div className="p-4 text-center text-xl font-bold">
            Start your conversation by selecting the documents you want to
            explore
          </div>
          <div className="h-1/8 flex w-full flex-wrap items-center justify-center font-nunito">
            <div className="m-1 flex w-96 items-center">
              <DocumentSelectCombobox
                selectedItem={selectedTicker}
                setSelectedItem={selectTicker}
                availableDocuments={availableTickers}
                shouldFocusTicker={shouldFocusCompanySelect}
                setFocusState={setShouldFocusCompanySelect}
              />
              <div className="flex h-[41px] w-[40px] items-center justify-center bg-[#F7F7F7] pr-3">
                <span className="mt-1 font-nunito text-[13px] font-bold text-[#7F7F7F]">
                  ⌘K
                </span>
              </div>
            </div>
            <div className="m-1 flex h-[41px] w-56 items-center bg-[#F7F7F7]">
              <div className="flex h-[41px] w-[30px] items-center justify-center bg-[#F7F7F7] pl-3">
                <CgFileDocument size={30} />
              </div>
              <div className="flex-grow">
                <Select
                  openMenuOnFocus
                  ref={documentTypeFocusRef}
                  options={availableDocumentTypes}
                  onChange={selectDocumentType}
                  getOptionLabel={(option: SelectOption) => option.label}
                  getOptionValue={(option: SelectOption) => option.value}
                  value={selectedDocumentType}
                  placeholder="Select Document Type"
                  components={{
                    IndicatorSeparator: () => null,
                    DropdownIndicator: () => null,
                  }}
                  styles={customReactSelectStyles}
                />
              </div>
            </div>
            <div className="m-1 flex h-[41px] w-48 items-center rounded-e bg-[#F7F7F7]">
              <div className="flex h-[41px] w-[30px] items-center justify-center bg-[#F7F7F7] pl-3">
                <AiTwotoneCalendar size={30} />
              </div>
              <div className="flex-grow">
                <Select
                  openMenuOnFocus
                  ref={yearFocusRef}
                  options={sortedAvailableYears || []}
                  getOptionLabel={(option: SelectOption) => option.label}
                  getOptionValue={(option: SelectOption) => option.value}
                  onChange={setSelectedYear}
                  value={selectedYear}
                  placeholder="Select Year"
                  components={{
                    IndicatorSeparator: () => null,
                    DropdownIndicator: () => null,
                  }}
                  styles={customReactSelectStyles}
                />
              </div>
            </div>
            <div className="relative">
              <button
                className="m-4 rounded border bg-llama-indigo px-8 py-2 text-white hover:bg-[#3B3775] disabled:bg-gray-30"
                onClick={handleAddDocument}
                disabled={!isDocumentSelectionEnabled || !selectedYear}
              >
                Add
              </button>

              <div className="absolute -right-[10px] bottom-[-4px] w-[140px] font-nunito text-[10px] text-[#7F7F7F]">
                {" "}
                <span className="font-bold">Shift + Enter </span>to add to list{" "}
              </div>
            </div>
          </div>

          <div className="mt-2 flex h-full w-11/12 flex-col justify-start overflow-scroll px-4 ">
            {selectedDocuments.length === 0 && (
              <div className="m-4 flex h-full flex-col items-center justify-center bg-gray-00 font-nunito text-gray-90">
                <div>
                  <CgFileDocument size={46} />
                </div>
                <div className="w-84 text-center md:w-64">
                  Use the document selector above to start adding documents
                </div>
              </div>
            )}
            {sortedSelectedDocuments.map((doc, index) => (
              <div
                key={index}
                className={cx(
                  index === 0 && "mt-2 border-t",
                  "group flex items-center justify-between border-b p-1 font-nunito font-bold text-[#868686] hover:bg-[#EAEAF7] hover:text-[#350F66] "
                )}
              >
                <div className="w-64 text-left">
                  <span className="font-bold">{doc.ticker}</span> -{" "}
                  {doc.fullName}
                </div>
                <div className="w-24 text-left">
                  {doc.year} {doc.quarter && `Q${doc.quarter}`}
                </div>
                <div>{doc.docType}</div>
                <button
                  className="mr-4 group-hover:text-[#FF0000]"
                  onClick={() => handleRemoveDocument(index)}
                >
                  <FiTrash2 size={24} />
                </button>
              </div>
            ))}
          </div>

          <div className="h-1/8 mt-2 flex w-full items-center justify-center rounded-lg bg-gray-00">
            <div className="flex flex-wrap items-center justify-center">
              {isDocumentSelectionEnabled && (
                <>
                  <div className="w-48 font-nunito md:ml-8 ">
                    Add up to{" "}
                    <span className="font-bold">
                      {" "}
                      {MAX_NUMBER_OF_SELECTED_DOCUMENTS -
                        selectedDocuments.length}
                    </span>{" "}
                    {isStartConversationButtonEnabled ? (
                      <>more docs</>
                    ) : (
                      <>docs</>
                    )}
                  </div>
                  <div className="ml-1 font-nunito ">
                    {isStartConversationButtonEnabled ? <>or</> : <>to</>}{" "}
                  </div>
                </>
              )}
              <div className="md:ml-12">
                <button
                  disabled={!isStartConversationButtonEnabled}
                  onClick={handleSubmit}
                  className={cx(
                    "m-4 rounded border bg-llama-indigo px-6 py-2 font-nunito text-white hover:bg-[#3B3775] disabled:bg-gray-30 ",
                    !isStartConversationButtonEnabled &&
                      "border-gray-300 bg-gray-300"
                  )}
                >
                  <div className="flex items-center justify-center">
                    {isLoadingConversation ? (
                      <div className="flex h-[22px] w-[180px] items-center justify-center">
                        <LoadingSpinner />
                      </div>
                    ) : (
                      <>
                        start your conversation
                        <div className="ml-2">
                          <AiOutlineArrowRight />
                        </div>
                      </>
                    )}
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
