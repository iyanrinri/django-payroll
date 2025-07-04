'use client';
import {useState} from "react";
import EmployeeForm from "@/app/(main)/employees/components/form";
import EmployeeList from "@/app/(main)/employees/components/list";

export default function Employees() {
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [refreshKey, setRefreshKey] = useState(0);
    const onSubmit = () => {
        setRefreshKey(prev => prev + 1);
        setShowCreateModal(false);
    }
    return (
        <div className="flex flex-col justify-start min-h-screen">
            <h1 className="text-4xl font-bold mb-4">Employees</h1>
            {showCreateModal && (
                <EmployeeForm onClose={() => setShowCreateModal(false)} onSubmit={onSubmit} />
            )}
            <div className="flex flex-col space-y-4 sm:flex-row justify-start sm:space-y-0 mb-4 gap-2">
                <button className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-900"
                        onClick={() => {setShowCreateModal(true)}}
                >
                    Create Employee
                </button>
            </div>
            <EmployeeList refreshKey={refreshKey}/>
        </div>
    )
}