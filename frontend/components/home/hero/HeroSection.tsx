import Image from "next/image";

export default function HeroSection() {
  return (
    <section>
      <div className="flex items-center justify-center md:h-[66vh] w-screen flex-col md:flex-row md:mx-auto bg-white">
        <div className="hero-content h-auto py-32 px-16">
          <h1 className="text-3xl font-semibold mb-1 text-gray-900">Lista de compras poderosa.</h1>
          <p className="mb-6 text-lg leading-8 text-gray-600">Com análise de preços em tempo real.</p>
          <a
            className="btn-primary md:w-50"
            href="/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Experimente agora
          </a>
        </div>
        <div className="hero-image h-auto md:max-w-[25%] mb-4">
          <Image
            src="/phone_14_01.png"
            alt="Imagem de Celular com PriceTeller Aberto"
            width={500}
            height={0}
          />
        </div>
      </div>
    </section>
  );
}