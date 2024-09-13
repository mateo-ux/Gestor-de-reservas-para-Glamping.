import Image from "next/image";
import Head from "next/head";
import Footer from "./components/footer/Footer";

export default function Home() {
  return (
    <main style={{background:'red'}}>
      <div>
        <Head>
          <title>proyecto1</title>
          <meta name="descripcion" content="generalidades de la app"/>
          <link rel="stylesheet" href="/favicon.ico" />
        </Head>

        
      </div>
    </main>
  );
}
