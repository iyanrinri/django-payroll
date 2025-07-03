import { useEffect, useState } from "react";

export default function Pagination({ page, perPage, total, onChangePage }) {
    const [pageNumbers, setPageNumbers] = useState([]);
    const [totalPage, setTotalPage] = useState(0);

    useEffect(() => {
        const totalPage = Math.ceil(total / perPage);
        const numbers = Array.from({ length: totalPage }, (_, i) => i + 1);
        setPageNumbers(numbers);
        setTotalPage(totalPage);
    }, [total, perPage]);

    return (
        <div className="flex flex-wrap items-center justify-between mt-4 gap-2">
            <button
                onClick={() => onChangePage(page - 1)}
                disabled={page <= 1}
                className="cursor-pointer px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 disabled:opacity-50"
            >
                Previous
            </button>

            <ul className="inline-flex space-x-1">
                {pageNumbers.map((p) => (
                    <li key={p}>
                        <button
                            onClick={() => onChangePage(p)}
                            className={`cursor-pointer px-3 h-8 text-sm rounded border border-gray-300 ${
                                p === page
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-white text-gray-700 hover:bg-gray-100'
                            }`}
                        >
                            {p}
                        </button>
                    </li>
                ))}
            </ul>

            <button
                onClick={() => onChangePage(page + 1)}
                disabled={page >= totalPage}
                className="cursor-pointer px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700 disabled:opacity-50"
            >
                Next
            </button>
        </div>
    );
}
