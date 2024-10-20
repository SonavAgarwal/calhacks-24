"use client"

import ImageDialog from "@/components/ImageDialog"
import { ItemsTable } from "@/components/items-table"
import { AlertDialog, AlertDialogContent } from "@/components/ui/alert-dialog"
import { Checkbox } from "@/components/ui/checkbox"
import { PLACEHOLDER_ITEMS } from "@/lib/data"
import { Image, Item, UploadSessionResponse } from "@/lib/types"
import {
    CellContext,
    ColumnDef,
    getCoreRowModel,
    useReactTable,
} from "@tanstack/react-table"
import { useParams, useSearchParams } from "next/navigation"
import { useEffect, useMemo, useRef, useState } from "react"
import { twMerge } from "tailwind-merge"

interface Props {}

const page = (props: Props) => {
    const { uploadId } = useParams()

    const before = useSearchParams().get("before") === "true"

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
                        {(info.getValue() as Image[])
                            .slice(0, 3)
                            .map((image, index) => (
                                <img
                                    onClick={() => setEnlargedImage(image)}
                                    key={image.id}
                                    src={image.url}
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

        console.log("data", data)

        if (before) {
            console.log("filtering")
            // only show rows that have an image with status pending
            data = data.filter((item) =>
                item.images.some((image) => image.status === "pending"),
            )

            // only show images with status pending
            data.forEach((item) => {
                item.images = item.images.filter(
                    (image) => image.status === "pending",
                )
            })
        } else {
            // only show rows that have an image with status pending and before is false
            data = data.filter((item) =>
                item.images.some(
                    (image) => image.status === "pending" && !image.before,
                ),
            )

            // // only show images with status pending and before is false
            // data.forEach((item) => {
            //     item.images = item.images.filter(
            //         (image) => image.status === "pending" && !image.before,
            //     )
            // })
        }
        console.log("data", data)
        return data
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
                    items: PLACEHOLDER_ITEMS,
                })
                console.log("response", response)
            }, 100)
        }

        fetchData()

        // return () => clearInterval(interval)
    }, [uploadId])

    const handleContinue = () => {
        const selectedRows = table.getSelectedRowModel().rows

        if (before) {
            // add to inventory
            console.log("Adding to inventory", selectedRows)
        } else {
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
                    We're processing your uploads. This may take a few minutes.
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

            <div className="flex min-h-screen w-full flex-col items-center gap-4 p-4 pt-12">
                <div className="flex w-full flex-row gap-4">
                    <div className="flex-1">
                        <h1 className="w-full text-2xl font-bold">
                            We found {items?.length} items!
                        </h1>
                        <p className="w-full text-base">
                            {before
                                ? "Select the ones you want to add to your inventory."
                                : "Select the ones you want to claim."}
                        </p>
                    </div>
                    <div className="flex flex-col gap-4">
                        <button
                            className="w-full rounded-lg bg-primary px-4 py-2 text-white transition-opacity disabled:opacity-50"
                            disabled={
                                table.getSelectedRowModel().rows.length === 0
                            }
                            onClick={handleContinue}
                        >
                            {before ? "Add to Inventory" : "Claim Items"}
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
                    )}
                </div>
            </div>
        </>
    )
}

export default page
