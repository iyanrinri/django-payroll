import {Geist, Geist_Mono} from "next/font/google";
import "../../globals.css";

const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
});

export const metadata = {
    title: "Payroll App",
    description: "Payroll App - Manage your payroll efficiently",
};

export default function LoginLayout({children}) {
    return (
        <section>{children}</section>
    );
}
