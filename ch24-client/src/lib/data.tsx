import { Claim, Item } from "./types"

export const PLACEHOLDER_ITEMS: Item[] = [
    {
        id: "1",
        name: "Placeholder Item 1",
        description: "This is a placeholder description for item 1.",
        price: 10.99,
        count: 5,
        category: "Category 1",
        images: [
            {
                id: "1a",
                url: "https://picsum.photos/seed/1a/200",
                status: "inventory",
                before: true,
            },
            {
                id: "1b",
                url: "https://picsum.photos/seed/1b/200",
                status: "pending",
                before: true,
            },
        ],
    },
    {
        id: "2",
        name: "Placeholder Item 2",
        description: "This is a placeholder description for item 2.",
        price: 15.49,
        count: 2,
        category: "Category 2",
        images: [
            {
                id: "2a",
                url: "https://picsum.photos/seed/2a/200",
                status: "rejected",
                before: true,
            },
        ],
    },
    {
        id: "3",
        name: "Placeholder Item 3",
        description: "This is a placeholder description for item 3.",
        price: 9.99,
        count: 10,
        category: "Category 1",
        images: [
            {
                id: "3a",
                url: "https://picsum.photos/seed/3a/200",
                status: "inventory",
                before: true,
            },
            {
                id: "3b",
                url: "https://picsum.photos/seed/3b/200",
                status: "pending",
                before: false,
            },
        ],
    },
    {
        id: "4",
        name: "Placeholder Item 4",
        description: "This is a placeholder description for item 4.",
        price: 25.0,
        count: 7,
        category: "Category 3",
        images: [
            {
                id: "4a",
                url: "https://picsum.photos/seed/4a/200",
                status: "inventory",
                before: true,
            },
            {
                id: "4b",
                url: "https://picsum.photos/seed/4b/200",
                status: "pending",
                before: false,
            },
            {
                id: "4c",
                url: "https://picsum.photos/seed/4c/200",
                status: "rejected",
                before: false,
            },
        ],
    },
    {
        id: "5",
        name: "Placeholder Item 5",
        description: "This is a placeholder description for item 5.",
        price: 5.75,
        count: 3,
        category: "Category 2",
        images: [
            {
                id: "5a",
                url: "https://picsum.photos/seed/5a/200",
                status: "inventory",
                before: true,
            },
        ],
    },
    {
        id: "6",
        name: "Placeholder Item 6",
        description: "This is a placeholder description for item 6.",
        price: 12.49,
        count: 6,
        category: "Category 1",
        images: [
            {
                id: "6a",
                url: "https://picsum.photos/seed/6a/200",
                status: "inventory",
                before: true,
            },
            {
                id: "6b",
                url: "https://picsum.photos/seed/6b/200",
                status: "pending",
                before: true,
            },
        ],
    },
    {
        id: "7",
        name: "Placeholder Item 7",
        description: "This is a placeholder description for item 7.",
        price: 8.99,
        count: 8,
        category: "Category 4",
        images: [
            {
                id: "7a",
                url: "https://picsum.photos/seed/7a/200",
                status: "rejected",
                before: false,
            },
            {
                id: "7b",
                url: "https://picsum.photos/seed/7b/200",
                status: "inventory",
                before: true,
            },
        ],
    },
    {
        id: "8",
        name: "Placeholder Item 8",
        description: "This is a placeholder description for item 8.",
        price: 19.95,
        count: 12,
        category: "Category 3",
        images: [
            {
                id: "8a",
                url: "https://picsum.photos/seed/8a/200",
                status: "inventory",
                before: true,
            },
        ],
    },
    {
        id: "9",
        name: "Placeholder Item 9",
        description: "This is a placeholder description for item 9.",
        price: 29.99,
        count: 1,
        category: "Category 5",
        images: [
            {
                id: "9a",
                url: "https://picsum.photos/seed/9a/200",
                status: "inventory",
                before: true,
            },
            {
                id: "9b",
                url: "https://picsum.photos/seed/9b/200",
                status: "pending",
                before: true,
            },
            {
                id: "9c",
                url: "https://picsum.photos/seed/9c/200",
                status: "rejected",
                before: false,
            },
        ],
    },
    {
        id: "10",
        name: "Placeholder Item 10",
        description: "This is a placeholder description for item 10.",
        price: 4.99,
        count: 15,
        category: "Category 2",
        images: [
            {
                id: "10a",
                url: "https://picsum.photos/seed/10a/200",
                status: "inventory",
                before: true,
            },
        ],
    },
]
