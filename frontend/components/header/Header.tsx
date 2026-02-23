import Logo from "./Logo"
import DesktopNav from "./DesktopNav";
import MobileMenuButton from "./MobileMenuButton";

export default function Header(){
    return(
        <header className="sticky top-0 z-50 backdrop-blur border-b bg-yellow-400"> 
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center md:justify-start md:gap-10"> 
                    <Logo />
                    <DesktopNav />
                    <MobileMenuButton />
                </div>
            </div>
        </header>
    )
}