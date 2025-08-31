import React from "react";
import QueryProvider from "./QueryProvider";

const Providers = async ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return <QueryProvider>{children}</QueryProvider>;
};

export default Providers;
