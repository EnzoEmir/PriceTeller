"use client";

import { useState } from "react";
import Link from "next/link";
import { headerLinks } from "./links";

export default function MobileMenuButton(){
    const [open, setOpen] = useState(false);
    return( 
    <div className="md:hidden">
      {/* Botão */}
      <button
        aria-expanded={open}
        aria-controls="mobile-menu"
        onClick={() => setOpen(!open)}
        className="p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-2xl"
      >
        ☰
      </button>
   
      {open && (
        <div
          id="mobile-menu"
          className="absolute left-0 top-16 w-full bg-black border-b shadow-md"
        >
          <nav className="flex flex-col p-4 gap-4">
            {headerLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className="transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </div>
    )
}