import Link from "next/link";

export function Nav() {
    return(
        <nav className="w-full h-20 bg-gray-50 border-b border-gray-200">
          <div className="w-full h-full max-w-7xl m-auto flex items-center">
            <p className="text-2xl">
              <Link href='/'>
                CRUD<span className="font-bold italic text-blue-900">SD</span>
              </Link>
            </p>
          </div>
        </nav>
    );
}