import Fuse from "fuse.js";
import { DocumentColorEnum, highlightColors } from "./colors";

interface WordData {
  text: string;
  spanIdx: number;
  wordIdx: number;
}

/*
 * This function works by breaking the doc up into
 * individual words, finding the longest contiguous sub-sequence
 * that matches the given textToHighlight, and directly
 * setting the background-color on the spans associated with the
 * longest contiguous sub-sequence.
 * TODO: I do wish it was easier to understand / cleaner
 */
export const multiHighlight = (
  textToHighlight: string,
  pageNumber: number,
  color = DocumentColorEnum.yellow
) => {
  const highlightColor = highlightColors[color];
  const spans = document.querySelectorAll(
    `div[data-page-number='${
      pageNumber + 1
    }'] .react-pdf__Page__textContent.textLayer span`
  );

  const words: WordData[] = [];
  spans.forEach((span, spanIdx) => {
    const htmlSpan = span as HTMLElement;
    const spanWords = htmlSpan.textContent || "";

    spanWords.split(" ").map((text, wordIdx) => {
      words.push({ text, spanIdx, wordIdx });
    });
  });

  let searchString = textToHighlight;
  searchString = searchString.replace(/\s{2,}/g, " ");
  searchString = searchString.replace(/\t/g, " ");
  searchString = searchString
    .toString()
    .trim()
    .replace(/(\r\n|\n|\r)/g, "");

  const searchWords = searchString.split(" ");
  const lenSearchString = searchWords.length;
  if (!lenSearchString) {
    return;
  }

  const firstWord = searchWords[0];
  if (!firstWord) {
    return;
  }
  const searchData = generateDirectSearchData(
    firstWord,
    words,
    lenSearchString
  );

  const options = {
    includeScore: true,
    threshold: 0.1, // Adjust this threshold according to your requirement.
    minMatchCharLength: 10, // You might want to increase this for sentences.
    shouldSort: true,
    findAllMatches: true,
    includeMatches: true,
    keys: ["text"], // This tells Fuse.js to search in the `text` property of the items in your list
  };

  const fuse = new Fuse(searchData, options);
  const result = fuse.search(searchString);

  if (result.length > 0) {
    const searchResult = result[0]?.item;

    const startSpan = searchResult?.startSpan || 0;
    const endSpan = searchResult?.endSpan || 0;
    const startWordIdx = searchResult?.startWordIdx || 0;
    const endWordIdx = searchResult?.endWordIdx || 0;

    for (let i = startSpan; i < endSpan + 1; i++) {
      const spanToHighlight = spans[i] as HTMLElement;
      if (i == startSpan) {
        if (startWordIdx === 0) {
          highlightHtmlElement(spanToHighlight, highlightColor);
        } else {
          partialHighlight(startWordIdx, spanToHighlight, DIRECTION.START);
        }
      } else if (i == endSpan) {
        if (endWordIdx === 0) {
          return;
        } else {
          partialHighlight(endWordIdx, spanToHighlight, DIRECTION.END);
        }
      } else {
        highlightHtmlElement(spanToHighlight, highlightColor);
      }
    }
  }
  return true;
};

const HIGHLIGHT_CLASSNAME = "opacity-40 saturate-[3] highlighted-by-llama ";

const highlightHtmlElement = (div: HTMLElement, color: string) => {
  const text = div.textContent || "";
  const newSpan = document.createElement("span");
  newSpan.className = HIGHLIGHT_CLASSNAME + color;
  newSpan.innerText = text;
  div.innerText = "";
  div.appendChild(newSpan);
};

enum DIRECTION {
  START,
  END,
}
const partialHighlight = (
  idx: number,
  span: HTMLElement,
  direction = DIRECTION.START
) => {
  const text = span.textContent;
  if (!text) {
    return;
  }
  const test = text.split(" ")[idx - 1] || "";
  const substringToHighlight = test; // replace this with the actual substring

  // Remove existing content in the span
  span.textContent = "";

  // Split the text into pieces by the substring
  const parts = text.split(substringToHighlight);

  // For each piece, append it and the highlighted substring (except for the last piece)
  parts.forEach((part, index) => {
    if (direction === DIRECTION.START) {
      if (index == 0) {
        span.appendChild(document.createTextNode(part));
      } else {
        span.appendChild(document.createTextNode(test));
        const highlightSpan = document.createElement("span");
        highlightSpan.className = HIGHLIGHT_CLASSNAME;
        highlightSpan.textContent = part;
        span.appendChild(highlightSpan);
      }
    }

    if (direction === DIRECTION.END) {
      if (index == 0) {
        const highlightSpan = document.createElement("span");
        highlightSpan.className = HIGHLIGHT_CLASSNAME;
        highlightSpan.textContent = part;
        span.appendChild(highlightSpan);
        // TODO: this is wrong, because it causes a double copy paste issue.
        // But without it, the offset is incorrect.
        span.appendChild(document.createTextNode(part));
      } else {
        span.appendChild(document.createTextNode(test));
        span.appendChild(document.createTextNode(part));
      }
    }
  });
};

interface SearchStrings {
  text: string;
  startSpan: number;
  endSpan: number;
  startWordIdx: number;
  endWordIdx: number;
}

function generateFuzzySearchData(arr: WordData[], n: number): SearchStrings[] {
  // used when we need to fuzzy search across the page
  const searchStrings: SearchStrings[] = [];

  for (let i = 0; i <= arr.length - n; i++) {
    // constructs sentence of length n
    const text = arr
      .slice(i, i + n)
      .reduce((acc, val) => acc + " " + val.text, "");

    const startSpan = arr[i]?.spanIdx || 0; // have to add these defaults because typescript is dumb
    const endSpan = arr[i + n]?.spanIdx || 0;
    const startWordIdx = arr[i]?.wordIdx || 0;
    const endWordIdx = arr[i + n]?.wordIdx || 0;
    searchStrings.push({ text, startSpan, endSpan, startWordIdx, endWordIdx });
  }

  return searchStrings;
}

function generateDirectSearchData(
  startString: string,
  words: WordData[],
  n: number
): SearchStrings[] {
  const searchStrings: SearchStrings[] = [];

  for (let i = 0; i <= words.length - n; i++) {
    if (words[i]?.text === startString) {
      // constructs sentence of length n
      const text = words
        .slice(i, i + n)
        .reduce((acc, val) => acc + " " + val.text, "");

      const startSpan = words[i]?.spanIdx || 0; // have to add these defaults because typescript is dumb
      const endSpan = words[i + n]?.spanIdx || 0;
      const startWordIdx = words[i]?.wordIdx || 0;
      const endWordIdx = words[i + n]?.wordIdx || 0;
      searchStrings.push({
        text,
        startSpan,
        endSpan,
        startWordIdx,
        endWordIdx,
      });
    }
  }

  return searchStrings;
}
