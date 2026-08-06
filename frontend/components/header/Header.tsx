import Logo from "./Logo";
import DesktopNav from "./DesktopNav";
import MobileMenuButton from "./MobileMenuButton";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-ink bg-accent">
      <div className="container-max">
        <div className="flex h-16 items-center justify-between gap-8">
          <Logo />
          <DesktopNav />
          <MobileMenuButton />
        </div>
      </div>
    </header>
  );
}
