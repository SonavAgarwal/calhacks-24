"use client"

import { flexRender, useReactTable } from "@tanstack/react-table"

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Item } from "@/lib/types"
import { Fragment } from "react"

interface ItemsTableProps<Item> {
    data: Item[]
    table: ReturnType<typeof useReactTable<Item>>
    onRowClick: (item: Item) => void
    expandedRow?: Item | null
}

export function ItemsTable<Items>({
    data,
    table,
    onRowClick,
    expandedRow,
}: ItemsTableProps<Item>) {
    return (
        <div className="rounded-md border">
            <Table>
                <TableHeader>
                    {table.getHeaderGroups().map((headerGroup) => (
                        <TableRow key={headerGroup.id}>
                            {headerGroup.headers.map((header) => {
                                return (
                                    <TableHead key={header.id}>
                                        {header.isPlaceholder
                                            ? null
                                            : flexRender(
                                                  header.column.columnDef
                                                      .header,
                                                  header.getContext(),
                                              )}
                                    </TableHead>
                                )
                            })}
                        </TableRow>
                    ))}
                </TableHeader>
                <TableBody>
                    {table.getRowModel().rows?.length ? (
                        table.getRowModel().rows.map((row, index) => (
                            <Fragment key={`fragment-${row.id}-${index}`}>
                                <TableRow
                                    key={`row-${row.id}-${index}`}
                                    data-state={
                                        row.getIsSelected() && "selected"
                                    }
                                    onClick={() => {
                                        onRowClick(row.original)
                                    }}
                                >
                                    {row.getVisibleCells().map((cell) => (
                                        <TableCell key={cell.id}>
                                            {flexRender(
                                                cell.column.columnDef.cell,
                                                cell.getContext(),
                                            )}
                                        </TableCell>
                                    ))}
                                </TableRow>
                                {expandedRow === row.original && (
                                    <TableRow
                                        key={`${row.id}-expanded`}
                                        data-state="expanded"
                                    >
                                        <TableCell
                                            colSpan={
                                                row.getVisibleCells().length
                                            }
                                        >
                                            <div className="flex flex-col">
                                                <div className="flex flex-row justify-center gap-4">
                                                    {[
                                                        "inventory",
                                                        "pending",
                                                    ].map((status) => {
                                                        const image =
                                                            row.original.images?.find(
                                                                (image) =>
                                                                    image.status ===
                                                                        status &&
                                                                    (status ===
                                                                    "inventory"
                                                                        ? image.before
                                                                        : !image.before),
                                                            )

                                                        if (!image) {
                                                            return null
                                                        }

                                                        return (
                                                            <div
                                                                key={image.url}
                                                                className="flex h-full flex-col items-center gap-2 rounded-lg border bg-white p-4"
                                                            >
                                                                <img
                                                                    key={
                                                                        image.url
                                                                    }
                                                                    src={
                                                                        image.url
                                                                    }
                                                                    className="h-64 flex-1 rounded-lg object-cover"
                                                                />
                                                                <h3 className="text-base">
                                                                    {status ===
                                                                    "inventory"
                                                                        ? `Before`
                                                                        : "After"}
                                                                </h3>
                                                            </div>
                                                        )
                                                    })}
                                                </div>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                )}
                            </Fragment>
                        ))
                    ) : (
                        <TableRow>
                            <TableCell
                                colSpan={table?.getAllColumns()?.length}
                                className="h-24 text-center"
                            >
                                No results.
                            </TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    )
}
