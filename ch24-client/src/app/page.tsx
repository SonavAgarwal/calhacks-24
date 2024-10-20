"use client"

import ImageDialog from "@/components/ImageDialog"
import { ItemsTable } from "@/components/items-table"
import { Checkbox } from "@/components/ui/checkbox"
import { Image, Item, UploadSessionResponse } from "@/lib/types"
import {
    CellContext,
    ColumnDef,
    getCoreRowModel,
    useReactTable,
} from "@tanstack/react-table"
import { match } from "assert"
import { useRouter, useSearchParams } from "next/navigation"
import { useEffect, useMemo, useRef, useState } from "react"
import { twMerge } from "tailwind-merge"

interface Props {}

const page = (props: Props) => {
    const before = useSearchParams().get("before") === "true"
    const router = useRouter()

    const [loading, setLoading] = useState(true)
    const processing = useRef(true)

    const [response, setResponse] = useState<UploadSessionResponse | null>(null)

    const [enlargedImage, setEnlargedImage] = useState<Image | null>(null)
    const [enlargedRow, setEnlargedRow] = useState<Item | null>(null)

    const itemColumns = useMemo(() => {
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
                accessorFn: (originalRow) =>
                    `$${parseFloat(originalRow.price).toFixed(2)}`,
            },
            {
                accessorKey: "before_count",
                header: "Count",
            },
            {
                accessorKey: "images",
                header: "Images",
                cell: (info: CellContext<Item, unknown>) => (
                    <div className="flex items-center justify-center">
                        {(info.getValue() as Image[])
                            .slice(0, 3)
                            .map((image, index) => (
                                <img
                                    onClick={() => setEnlargedImage(image)}
                                    key={image.image_id}
                                    src={image.url_path}
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
            {
                accessorKey: "id",
                header: "",
                cell: ({ row }: CellContext<Item, unknown>) => (
                    <Checkbox
                        onClick={(e) => e.stopPropagation()}
                        className="mr-4 h-6 w-6"
                        checked={row.getIsSelected()}
                        onCheckedChange={row.getToggleSelectedHandler()}
                    />
                ),
            },
        ]
        return itemsColumns
    }, [response])

    const items = useMemo<Item[]>(() => {
        // filter items based on before
        let data = response?.items ?? []
        return data
    }, [before, response])

    const matchedItems = useMemo<Item[]>(() => {
        // filter items based on before
        // let data = []
        return []
    }, [before, response])

    const table = useReactTable({
        data: items,
        columns: itemColumns,
        getCoreRowModel: getCoreRowModel(),
        getRowId: (row) => row.id,
        enableRowSelection: true,
        enableMultiRowSelection: true,
    })

    useEffect(() => {
        function fetchData() {
            fetch(
                `${process.env.NEXT_PUBLIC_BASE_URL}/inventory?status=inventory`,
                {
                    headers: {
                        "ngrok-skip-browser-warning": "true",
                    },
                },
            )
                .then((response) => response.json())
                .then((data) => {
                    setLoading(false)
                    processing.current = data.processing
                    setResponse(data)
                    console.log("data", data)
                })
                .catch((error) => {
                    console.error("Error fetching data", error)
                })

            setLoading(false)
        }

        fetchData()

        // return () => clearInterval(interval)
    }, [])

    const claimItems = () => {
        const selectedRows = table.getSelectedRowModel()?.rows ?? []
        // claim items
        console.log("Claiming items", selectedRows)
        // store in local storage
        localStorage.setItem(
            "claimedItems",
            JSON.stringify(selectedRows.map((row) => row.original)),
        )

        // open /pdf in a new tab
        window.open("/pdf", "_blank")
    }

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
                    We're fetching everything. This may take a few minutes.
                </p>
            </div>
        )
    }

    if (!response) {
        return <div>error</div>
    }

    return (
        <>
            <ImageDialog
                enlargedImage={enlargedImage}
                setEnlargedImage={setEnlargedImage}
            />
            <div className="flex min-h-screen w-screen flex-col items-center">
                <div className="flex min-h-screen w-[48rem] flex-col">
                    <div className="flex min-h-screen w-full flex-col items-center gap-4 p-4 pt-12">
                        <div className="flex w-full flex-row gap-4">
                            <div className="flex-1">
                                <h1 className="w-full text-2xl font-bold">
                                    Your inventory has {items?.length} items.
                                </h1>
                                <p className="w-full text-base">
                                    {before
                                        ? "Select the ones you want to add to your inventory."
                                        : "Select the ones you want to claim."}
                                </p>
                            </div>
                            <div className="flex items-start gap-4">
                                <button
                                    className="rounded-lg border border-border bg-background px-4 py-2 text-black"
                                    onClick={() => {
                                        router.push("/upload")
                                    }}
                                >
                                    Add Items
                                </button>
                                <button
                                    className="rounded-lg bg-primary px-4 py-2 text-white disabled:opacity-50"
                                    onClick={() => {
                                        claimItems()
                                    }}
                                    disabled={
                                        table.getSelectedRowModel()?.rows
                                            .length === 0
                                    }
                                >
                                    Claim Items
                                </button>
                            </div>
                        </div>

                        <div className="flex w-full flex-col gap-4">
                            {processing.current &&
                                new Array(3)
                                    .fill(0)
                                    .map((_, index) => (
                                        <div
                                            key={index}
                                            className="flex min-h-16 animate-pulse flex-col gap-2 rounded-lg bg-background p-4"
                                        ></div>
                                    ))}

                            {!processing.current && response && (
                                <>
                                    <ItemsTable
                                        data={response.items}
                                        table={table}
                                        onRowClick={(item) => {
                                            if (before) return
                                            if (enlargedRow === item) {
                                                setEnlargedRow(null)
                                                return
                                            }
                                            setEnlargedRow(item)
                                        }}
                                        expandedRow={enlargedRow}
                                    />
                                    {matchedItems.length > 0 && (
                                        <>
                                            <div className="flex w-full flex-col">
                                                <h1 className="w-full text-xl font-bold">
                                                    Matched Items
                                                </h1>
                                                <p className="w-full text-base">
                                                    These are items that you've
                                                    already found.
                                                </p>
                                            </div>
                                            <ItemsTable
                                                data={matchedItems}
                                                table={table}
                                                onRowClick={(item) => {
                                                    if (before) return
                                                    if (enlargedRow === item) {
                                                        setEnlargedRow(null)
                                                        return
                                                    }
                                                    setEnlargedRow(item)
                                                }}
                                                expandedRow={enlargedRow}
                                            />
                                        </>
                                    )}
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default page
