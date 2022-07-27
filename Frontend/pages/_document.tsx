import Document, { Html, Head, Main, NextScript } from "next/document";
import Script from "next/script";

class MyDocument extends Document {
  render() {
    return (
      <Html>
        <Head>
          {/* <link
            href="https://fonts.googleapis.com/css2?family=Inter&display=optional"
            rel="stylesheet"
          /> */}
          {/* <link rel="preconnect" href="https://fonts.gstatic.com"  /> */}
          <link
            href="https://fonts.googleapis.com/css2?family=Lato:wght@100;300;400;700;900&display=swap"
            rel="stylesheet"
          />
        </Head>
        <body className="font-Lato m-0 text-[#0B1A30]  bg-body-bg bg-repeat bg-left-top bg-[length:200px_100px] -mb-96">
          <div className="w-full h-full bg-[#F9F9FC]/90 -mb-96">

          <Main />
          <NextScript />
          </div>
          
        </body>
        {/* <script src="//cdn.jsdelivr.net/npm/eruda"></script> */}
      </Html>
    );
  }
}

export default MyDocument;
