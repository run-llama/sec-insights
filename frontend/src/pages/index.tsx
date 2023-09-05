import React from "react";

import type { NextPage } from "next";
import { MarketingSection } from "~/components/landing-page/MarketingSection";
import { TitleAndDropdown } from "~/components/landing-page/TitleAndDropdown";

const LandingPage: NextPage = () => {
  return (
    <>
      <TitleAndDropdown />
      <MarketingSection />
    </>
  );
};
export default LandingPage;
