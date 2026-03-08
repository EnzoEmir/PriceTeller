import Link from "next/link";


export default function DesktopNav(){

    const links = [
        { href: "/", label: "Página Inicial" },
        { href: "/pricing", label: "Planos" },
        { href: "/about", label: "Sobre Nós" },
    ];

    return (
    <nav className="hidden md:flex items-center gap-6">
      {links.map((link) => (
        <Link
          key={link.href}
          href={link.href}
          className="text-sm font-medium text-white-700 hover:text-blue-600 transition-colors"
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}