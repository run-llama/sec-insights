import { NextPageContext } from "next";
import React from "react";

interface ErrorProps {
  statusCode?: number;
}

const ErrorPage = ({ statusCode }: ErrorProps): JSX.Element => {
  return (
    <p>
      {statusCode
        ? `An error ${statusCode} occurred on server`
        : "An error occurred on client"}
    </p>
  );
};

ErrorPage.getInitialProps = ({ res, err }: NextPageContext) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default ErrorPage;
