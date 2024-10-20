import {
    CellContext,
    ColumnDef,
    createColumnHelper,
} from "@tanstack/react-table"

export interface Item {
    id: string
    name: string
    description: string
    price: number
    count: number
    category: string
    images: Image[]
}

export interface Image {
    id: string
    url: string
    status: "pending" | "inventory" | "rejected"
    before: boolean
}

export interface Claim {
    id: number
    name: string
    dateFiled: Date
    items: Item[]
}

export interface UploadSessionResponse {
    id: string
    date: Date
    after: boolean
    processing: boolean
    items: Item[]
}
