// we have to use react-pdf 6.2.2 instead of
// 7.^ because of a known text-layer issue.
// There are no types for this early version,
// so we need to declare a module file to get
// rid of type compilation issues
declare module "react-pdf";
