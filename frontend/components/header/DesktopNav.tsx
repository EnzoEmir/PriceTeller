import Link from "next/link";
import { headerLinks } from "./links";


export default function DesktopNav(){

    return (
    <nav className="hidden md:flex items-center gap-6">
      {headerLinks.map((link) => (
        <Link
          key={link.href}
          href={link.href}
          className="text-sm font-medium transition-colors"
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}