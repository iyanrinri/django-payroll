import {useEffect, useState} from "react";
import {toast} from "react-hot-toast";
import Pagination from "@/components/pagination";
import ConfirmDeletion from "@/components/confirm-deletion";
import EmployeeForm from "@/app/(main)/employees/components/form";

export default function EmployeeList({refreshKey}) {
    const [itemData, setItemData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalItems, setTotalItems] = useState(0);
    const [selectedItem, setSelectedItem] = useState(null);
    const [showFormModal, setShowFormModal] = useState(false);
    const [confirmationDelete, setConfirmationDelete] = useState(false);
    const [message, setMessage] = useState('');

    const handleEdit = (item) => {
        setSelectedItem(item);
        setShowFormModal(true)
    }
    const onSubmit = () => {
        setShowFormModal(false);
        setSelectedItem(null);
        setPage(1);
        fetchItems();
    }

    const showConfirmation = (item) => {
        setSelectedItem(item);
        setMessage(`Are you sure you want to delete the item for: ${item.clock_date_display} with employee: "${item.hours} hours" ?`);
        setConfirmationDelete(true);
    }

    const handleDelete = async () => {
        try {
            const response = await fetch(`/api/employees/${selectedItem.id}`, {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json',
                },
            });

            if (!response.ok) {
                toast.error('Failed to delete item');
                return;
            }

            toast.success('Item deleted successfully');
            fetchItems();
        } catch (error) {
            toast.error('Network error');
        } finally {
        }
    }
    const fetchItems = async () => {
        setLoading(true);
        try {
            const response = await fetch(`/api/employees?paginated=1&page=${page}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                },
            });

            if (!response.ok) {
                toast.error('Failed to fetch reimbursements');
                return;
            }

            const data = await response.json();
            setItemData(data);
            setPerPage(data.per_page || 10);
            setTotalItems(data.count || 0);
        } catch (error) {
            toast.error('Network error');
        } finally {
            setLoading(false);
        }
    };

    const changePage = (newPage) => {
        if (newPage >= 1) {
            setPage(newPage);
        }
    };

    useEffect(() => {
        fetchItems();
    }, [page, refreshKey]);

    return (
        <div className="relative overflow-x-auto">
            {showFormModal && (
                <EmployeeForm item={selectedItem} onClose={() => setShowFormModal(false)} onSubmit={onSubmit} />
            )}
            {confirmationDelete && (
                <ConfirmDeletion message={message} onConfirm={handleDelete} onCancel={() => {
                    setConfirmationDelete(false);
                    setSelectedItem(null);
                }} />
            )}

            {loading ? (
                'fetching data items...'
            ) : (
                <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th className="px-6 py-3">Name</th>
                        <th className="px-6 py-3">Email</th>
                        <th className="px-6 py-3">Base Salary</th>
                        <th className="px-6 py-3">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {itemData && itemData.results.map((item, index) => (
                        <tr key={index}
                            className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
                            <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                {item.name || 'N/A'}
                            </td>
                            <td className="px-6 py-4">{item.email || 'N/A'}</td>
                            <td className="px-6 py-4">{item.salary || 'N/A'}</td>
                            <td className="px-6 py-4">
                                <div className="flex items-center space-x-2">
                                    <button
                                        onClick={() => {
                                            handleEdit(item);
                                        }}
                                        className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-900 cursor-pointer"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => {
                                            showConfirmation(item);
                                        }}
                                        className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-900 cursor-pointer"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            )}

            <Pagination
                page={page}
                perPage={perPage}
                total={totalItems}
                onChangePage={changePage}
            />
        </div>
    );
}
