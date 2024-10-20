"use client"

import { ItemsTable } from "@/components/items-table"
import { Checkbox } from "@/components/ui/checkbox"
import { items } from "@/lib/data"
import { Item, UploadSessionResponse } from "@/lib/types"
import {
    CellContext,
    ColumnDef,
    getCoreRowModel,
    useReactTable,
} from "@tanstack/react-table"
import { useParams } from "next/navigation"
import { useEffect, useMemo, useRef, useState } from "react"
import { twMerge } from "tailwind-merge"

interface Props {}

const page = (props: Props) => {
    const { uploadId } = useParams()

    const [loading, setLoading] = useState(true)
    const processing = useRef(true)

    const [response, setResponse] = useState<UploadSessionResponse | null>(null)

    const [selectedItemIds, setSelectedItemIds] = useState<string[]>([])

    const itemColumns = useMemo(() => {
        const data = response?.items ?? []
        const itemsColumns: ColumnDef<Item>[] = [
            {
                accessorKey: "name",
                header: "Name",
            },
            {
                accessorKey: "description",
                header: "Description",
                cell: (info: CellContext<Item, unknown>) => (
                    <div className="text-sm">
                        {info.row.original.description}
                    </div>
                ),
            },
            {
                accessorKey: "price",
                header: "Price",
                accessorFn: (originalRow) => `$${originalRow.price.toFixed(2)}`,
            },
            {
                accessorKey: "count",
                header: "Count",
            },
            {
                accessorKey: "images",
                header: "Images",
                cell: (info: CellContext<Item, unknown>) => (
                    <div className="flex items-center justify-center">
                        {(info.getValue() as string[])
                            .slice(0, 3)
                            .map((image, index) => (
                                <img
                                    // onClick={}
                                    key={image}
                                    src={image}
                                    alt={info.row.original.name}
                                    className={twMerge(
                                        "h-10 w-10 rounded-md border-2 border-white object-cover",
                                    )}
                                    style={{
                                        marginLeft: index === 0 ? 0 : "-1.5rem",
                                    }}
                                />
                            ))}
                    </div>
                ),
            },
            {
                accessorKey: "category",
                header: "Category",
            },
            // checkbox column
            {
                accessorKey: "id",
                header: "",
                cell: ({ row }: CellContext<Item, unknown>) => (
                    <Checkbox
                        className="mr-4 h-6 w-6"
                        checked={row.getIsSelected()}
                        onCheckedChange={row.getToggleSelectedHandler()}
                    />
                ),
            },
        ]
        return itemsColumns
    }, [response])

    const table = useReactTable({
        data: response?.items ?? [],
        columns: itemColumns,
        getCoreRowModel: getCoreRowModel(),
        getRowId: (row) => row.id,
        enableRowSelection: true,
        enableMultiRowSelection: true,
    })

    useEffect(() => {
        // fetch example.com/upload/${uploadId}
        // if successful, set loading to false

        // if response.processing is true, set processing to true
        // if not, set processing to false

        // if not, show error

        function fetchData() {
            // fetch(`https://example.com/upload/${uploadId}`)
            //     .then((response) => response.json())
            //     .then((data) => {
            //         setLoading(false)
            //         processing.current = data.processing
            //     })
            //     .catch((error) => {
            //         console.error("Error fetching data")
            //     })

            setLoading(false)

            setTimeout(() => {
                processing.current = false
                setLoading(false)
                setResponse({
                    id: "123",
                    date: new Date(),
                    after: false,
                    processing: false,
                    items: items,
                })
            }, 1000)
        }

        const interval = setInterval(() => {
            if (processing.current) {
                fetchData()
            }
        }, 0)

        return () => clearInterval(interval)
    }, [uploadId])

    if (loading || processing.current) {
        return (
            <div className="flex min-h-screen w-full flex-col items-center justify-center gap-4">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="64"
                    height="64"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className={twMerge("animate-spin")}
                >
                    <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                </svg>
                <h1 className="w-full text-center text-2xl font-bold">
                    Hang tight!
                </h1>
                <p className="w-full text-center text-base">
                    We're processing your uploads. This may take a few minutes.
                </p>
            </div>
        )
    }

    if (!response) {
        return <div>error</div>
    }

    return (
        <div className="flex min-h-screen w-full flex-col items-center gap-4 p-4 pt-12">
            <div className="flex w-full flex-row gap-4">
                <div className="flex-1">
                    <h1 className="w-full text-2xl font-bold">
                        We found {response.items.length} items!
                    </h1>
                    <p className="w-full text-base">
                        Select the ones you want to add to your inventory.
                    </p>
                </div>
                <div className="flex flex-col gap-4">
                    <button
                        className="w-full rounded-lg bg-primary px-4 py-2 text-white transition-opacity disabled:opacity-50"
                        disabled={table.getSelectedRowModel().rows.length === 0}
                    >
                        Add to {response.after ? "Claims" : "Inventory"}
                    </button>
                </div>
            </div>

            <div className="flex w-full flex-col gap-4">
                {processing.current &&
                    new Array(3).fill(0).map((_, index) => (
                        // skeleton
                        <div
                            key={index}
                            className="flex min-h-16 animate-pulse flex-col gap-2 rounded-lg bg-background p-4"
                        ></div>
                    ))}

                {!processing.current && response && (
                    <ItemsTable data={response.items} table={table} />
                )}
            </div>
        </div>
    )
}

export default page
