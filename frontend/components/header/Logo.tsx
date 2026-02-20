"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";

interface LogoProps {
  src?: string;
  alt?: string;
  textFallback?: string;
}

export default function Logo({
  src = "/logo.png",
  alt = "Logo",
  textFallback = "MyApp",
}: LogoProps) {
  const [error, setError] = useState(false);

  return (
    <Link href="/" className="flex items-center">
      {!error ? (
        <Image
          src={src}
          alt={alt}
          width={120}
          height={40}
          priority
          onError={() => setError(true)}
          className="object-contain"
        />
      ) : (
        <span className="text-xl font-bold tracking-tight">
          {textFallback}
        </span>
      )}
    </Link>
  );
}