export default function Card({title, description, children}) {
    return (
        <div
            className="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
            <h3 className="text-2xl font-bold mb-5">{title}</h3>
            <p className="mb-5 text-gray-600 dark:text-gray-400">{description}</p>
            {children}
        </div>
    );
}