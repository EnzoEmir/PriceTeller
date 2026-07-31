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
  alt = "PriceTeller",
  textFallback = "PriceTeller",
}: LogoProps) {
  const [error, setError] = useState(false);

  return (
    <Link href="/" className="flex items-center gap-2">
      {!error && (
        <Image
          src={src}
          alt={alt}
          width={36}
          height={36}
          priority
          onError={() => setError(true)}
          className="object-contain"
        />
      )}
      <span className="font-display text-xl font-bold tracking-tight">
        {textFallback}
      </span>
    </Link>
  );
}