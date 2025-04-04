import Link from "next/link";

export default function Header() {
    const generateLinks = () => {
        const links = ["Home", "Stores"];
        return links.map((link, index) => (
            <li key={index} className="px-4 py-2 mr-4">
                <Link href="#" className="hover:underline">
                    {link}
                </Link>
            </li>
        ));
    };

    return (
        <div className="border-b dark:border-b-white">
            <nav>
                <ul className="flex flex-row">{generateLinks()}</ul>
            </nav>
        </div>
    );
}
