import {useEffect, useState} from "react";
import {toast} from "react-hot-toast";
import Pagination from "@/components/pagination";
import ReimbursementForm from "@/app/reimbursements/components/form";
import ConfirmDeletion from "@/components/confirm_deletion";

export default function ReimbursementList({refreshKey}) {
    const [reimbursementData, setReimbursementData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalItems, setTotalItems] = useState(0);
    const [selectedReimbursement, setSelectedReimbursement] = useState(null);
    const [showFormModal, setShowFormModal] = useState(false);
    const [confirmationDelete, setConfirmationDelete] = useState(false);
    const [message, setMessage] = useState('');

    const handleEdit = (reimbursement) => {
        setSelectedReimbursement(reimbursement);
        setShowFormModal(true)
    }
    const onSubmit = () => {
        setShowFormModal(false);
        setSelectedReimbursement(null);
        setPage(1);
        fetchReimbursements();
    }

    const showConfirmation = (reimbursement) => {
        setSelectedReimbursement(reimbursement);
        setMessage(`Are you sure you want to delete the reimbursement for: ${reimbursement.claim_date_display} with amount ${reimbursement.amount_display} description: ${reimbursement.description || 'N/A'}?`);
        setConfirmationDelete(true);
    }

    const handleDelete = async () => {
        try {
            const response = await fetch(`/api/reimbursements/${selectedReimbursement.id}`, {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json',
                },
            });

            if (!response.ok) {
                toast.error('Failed to delete reimbursement');
                return;
            }

            toast.success('Reimbursement deleted successfully');
            fetchReimbursements();
        } catch (error) {
            toast.error('Network error');
        } finally {
        }
    }
    const fetchReimbursements = async () => {
        setLoading(true);
        try {
            const response = await fetch(`/api/reimbursements?page=${page}`, {
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
            setReimbursementData(data);
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
        fetchReimbursements();
    }, [page, refreshKey]);

    return (
        <div className="relative overflow-x-auto">
            {showFormModal && (
                <ReimbursementForm reimbursement={selectedReimbursement} onClose={() => setShowFormModal(false)} onSubmit={onSubmit} />
            )}
            {confirmationDelete && (
                <ConfirmDeletion message={message} onConfirm={handleDelete} onCancel={() => {
                    setConfirmationDelete(false);
                    setSelectedReimbursement(null);
                }} />
            )}

            {reimbursementData && reimbursementData?.count > 0 && !loading ? (
                <div className="py-4">
                    <span>Total Claimed Amount: <span
                        className="font-bold">{reimbursementData.total_amount_display}</span></span>
                </div>
            ) : null}

            {loading ? (
                'fetching data reimbursements...'
            ) : (
                <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                        <th className="px-6 py-3">Claim Date</th>
                        <th className="px-6 py-3">Amount</th>
                        <th className="px-6 py-3">Description</th>
                        <th className="px-6 py-3">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {reimbursementData && reimbursementData.results.map((reimbursement, index) => (
                        <tr key={index}
                            className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
                            <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                {reimbursement.claim_date_display || 'N/A'}
                            </td>
                            <td className="px-6 py-4">{reimbursement.amount_display || 'N/A'}</td>
                            <td className="px-6 py-4">{reimbursement.description || 'N/A'}</td>
                            <td className="px-6 py-4">
                                <div className="flex items-center space-x-2">
                                    <button
                                        onClick={() => {
                                            handleEdit(reimbursement);
                                        }}
                                        className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-900 cursor-pointer"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => {
                                            showConfirmation(reimbursement);
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
