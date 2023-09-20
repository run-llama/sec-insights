/* eslint-disable react/jsx-key */
import React from "react";
import AnimateSvg from "./AnimateSvg";
import useScrollBreakpoint from "~/hooks/utils/useScrollBreakpoint";

export const MarketingSection = () => {
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };
  const { ref: chatRef, breakpoint: chatBreakpoint } = useScrollBreakpoint(100);
  const { ref: multiDocRef, breakpoint: multiDocBreakpoint } =
    useScrollBreakpoint();
  const { ref: highlightRef, breakpoint: highlightBreakpoint } =
    useScrollBreakpoint();

  return (
    <>
      <div className="mb-24 mt-24 flex h-max min-h-[200px] w-full items-center justify-center">
        <div className="flex flex-col items-center justify-center">
          <div className="font-bold text-llama-indigo">
            SEC Insights presents
          </div>
          <div className="w-3/4 text-center font-lora text-4xl font-bold">
            The next step in analyzing complex financial documents
          </div>
        </div>
      </div>
      <div className="landing-page-gradient-2 mt-16 flex h-max min-h-[500px] w-full flex-col-reverse items-center justify-center sm:mt-0 sm:flex-row">
        <div
          ref={chatRef}
          className="mb-5 mt-5 flex w-full items-center justify-center sm:mb-0 sm:mt-0 sm:w-1/2"
        >
          <AnimateSvg
            breakpoint={chatBreakpoint}
            increment={80}
            svgs={[
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="chat-1.svg"
              />,
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="chat-2.svg"
              />,
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="chat-3.svg"
              />,
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="chat-4.svg"
              />,
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="chat-5.svg"
              />,
            ]}
          />
        </div>

        <div className="w-full text-center sm:w-1/2 sm:text-left">
          <div className="sm:3/5 mx-auto w-4/5 text-3xl font-bold sm:mx-0">
            Take a peek under the hood and stream insights directly from the
            algorithm
          </div>
          <div className="sm:3/5 mx-auto mt-3 w-4/5 font-lora text-xl sm:mx-0">
            SEC Insights does more than give you the answer. It helps you
            understand how that answer was generated in the first place.
          </div>
        </div>
      </div>
      <div className="landing-page-gradient-3 mx-auto flex h-max min-h-[500px] w-4/5 flex-col items-center justify-center sm:flex-row">
        <div className="w-full text-center text-center sm:w-1/2 sm:text-left">
          <div className="mx-auto w-4/5 text-3xl font-bold sm:w-4/5 ">
            Extract meaningful insight from inquiries across multiple documents
          </div>
          <div className="mx-auto mt-3 w-4/5 font-lora text-xl sm:w-4/5 ">
            With the ability to simultaneously examine multiple documents, SEC
            Insights provides comprehensive insights, enabling deep comparisons
            and contrasts.
          </div>
        </div>
        <div
          ref={multiDocRef}
          className="mb-5 mt-5 flex w-full items-center justify-center sm:mb-0 sm:mt-0 sm:w-1/2 sm:justify-center"
        >
          <AnimateSvg
            breakpoint={multiDocBreakpoint}
            increment={150}
            svgs={[
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="multi-doc-4.svg"
              />,
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="multi-doc-2.svg"
              />,
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="multi-doc-3.svg"
              />,
            ]}
          />
        </div>
      </div>
      <div className="landing-page-gradient-3 mx-auto flex h-max min-h-[500px] w-4/5 flex-col items-center justify-center sm:flex-row">
        <div className="w-full text-center sm:w-1/2 sm:text-left">
          <div className="mx-auto w-4/5 text-3xl font-bold sm:w-4/5 ">
            Dive deeper into your response by viewing citations at the paragraph
            level
          </div>
          <div className="mx-auto mt-3 w-4/5 font-lora text-xl sm:w-4/5 ">
            Navigate through dense financial information with precision. Our
            tool guides you to paragraph-level citations across multiple
            documents, enabling an unmatched level of clarity and comprehension.
          </div>
        </div>
        <div
          ref={highlightRef}
          className="mb-5 mt-5 flex w-full items-center justify-center sm:mb-0 sm:mt-0 sm:w-1/2 sm:justify-center"
        >
          <AnimateSvg
            breakpoint={highlightBreakpoint}
            increment={150}
            svgs={[
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="highlight-4.svg"
              />,
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="highlight-2.svg"
              />,
              <img
                className="max-w-[350px] sm:max-w-[400px]"
                src="highlight-1.svg"
              />,
            ]}
          />
        </div>
      </div>
      <div className="landing-page-gradient-4">
        <div className="flex items-center justify-center">
          <div className="flex h-max min-h-[300px] w-3/4 items-center justify-center">
            <div className="flex flex-col items-center justify-center rounded-lg border bg-white p-4">
              <div className="w-3/4 text-center font-lora text-3xl font-bold">
                Interested? Get in touch to discuss enterprise use cases or
                provide feedback
              </div>
              <div className="flex items-center justify-around">
                <a href="mailto:hi@secinsights.ai" target="_blank">
                  <button className="m-4 rounded border bg-llama-indigo px-8 py-2 font-bold text-white hover:bg-[#3B3775]">
                    Get in Touch
                  </button>
                </a>
              </div>
            </div>
          </div>
        </div>

        <div className="item-center mt-10 flex justify-center pb-10 text-center">
          <div className="flex flex-col text-gray-60">
            <button
              onClick={scrollToTop}
              className="mb-4 font-bold text-gray-90"
            >
              Back to Top
            </button>
            <div>©LlamaIndex Inc. 2023. All rights reserved.</div>
          </div>
        </div>
      </div>
    </>
  );
};
