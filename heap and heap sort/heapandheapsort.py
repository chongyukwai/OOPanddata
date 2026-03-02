"""
COMPREHENSIVE HEAP DATA STRUCTURE & ALGORITHMS
Complete implementation from scratch without external libraries
Author: Self-Study Implementation
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import time
import math

# ============================================================================
# HEAP DATA STRUCTURE IMPLEMENTATIONS
# ============================================================================

class Heap:
    """
    Base Heap Class - Foundation for all heap implementations
    Contains core heap logic that can be extended for different heap types
    """
    
    def __init__(self, heap_type='max'):
        """
        Initialize heap
        Args:
            heap_type: 'max' for max heap, 'min' for min heap
        """
        self.heap = []
        self.type = heap_type
        self.comparisons = 0
        self.swaps = 0
        self.operations_log = []
    
    # ========== INDEX HELPER FUNCTIONS ==========
    
    def parent(self, i):
        """Get parent index (0-based indexing)"""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Get left child index"""
        return 2 * i + 1
    
    def right_child(self, i):
        """Get right child index"""
        return 2 * i + 2
    
    def is_leaf(self, i):
        """Check if node at index i is a leaf"""
        n = len(self.heap)
        return i >= n // 2
    
    def get_level(self, i):
        """Get level of node at index i (root is level 0)"""
        level = 0
        while i > 0:
            i = self.parent(i)
            level += 1
        return level
    
    def get_height(self):
        """Get height of the heap"""
        n = len(self.heap)
        height = 0
        while (1 << height) - 1 < n:  # 2^height - 1
            height += 1
        return height
    
    # ========== COMPARISON AND SWAP ==========
    
    def compare(self, a, b):
        """
        Compare two elements based on heap type
        For max heap: a > b returns True
        For min heap: a < b returns True
        """
        self.comparisons += 1
        if self.type == 'max':
            return a > b
        else:
            return a < b
    
    def swap(self, i, j):
        """Swap elements at indices i and j"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.swaps += 1
        self.operations_log.append(f"Swapped indices {i} and {j}: {self.heap}")
    
    # ========== CORE HEAP OPERATIONS ==========
    
    def insert(self, value):
        """
        Insert value into heap
        Time Complexity: O(log n)
        
        Algorithm:
        1. Add element at the end
        2. Bubble up until heap property restored
        """
        self.operations_log.append(f"Inserting {value}")
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)
        self.operations_log.append(f"After insert: {self.heap}")
        return self
    
    def _sift_up(self, i):
        """
        Move element up to maintain heap property
        Time Complexity: O(log n)
        """
        while i > 0 and self.compare(self.heap[i], self.heap[self.parent(i)]):
            self.swap(i, self.parent(i))
            i = self.parent(i)
    
    def extract_root(self):
        """
        Extract root element (max for max heap, min for min heap)
        Time Complexity: O(log n)
        
        Algorithm:
        1. Save root value
        2. Move last element to root
        3. Bubble down until heap property restored
        """
        if not self.heap:
            return None
        
        self.operations_log.append("Extracting root")
        
        if len(self.heap) == 1:
            value = self.heap.pop()
            self.operations_log.append(f"Extracted {value}, heap now empty")
            return value
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        
        self.operations_log.append(f"Extracted {root}, heap now: {self.heap}")
        return root
    
    def _sift_down(self, i):
        """
        Move element down to maintain heap property
        Time Complexity: O(log n)
        """
        n = len(self.heap)
        
        while True:
            left = self.left_child(i)
            right = self.right_child(i)
            extreme = i  # largest for max heap, smallest for min heap
            
            # Compare with left child
            if left < n and self.compare(self.heap[left], self.heap[extreme]):
                extreme = left
            
            # Compare with right child
            if right < n and self.compare(self.heap[right], self.heap[extreme]):
                extreme = right
            
            # If heap property satisfied, break
            if extreme == i:
                break
            
            # Swap with extreme child and continue
            self.swap(i, extreme)
            i = extreme
    
    def build_heap(self, arr):
        """
        Build heap from array
        Time Complexity: O(n)
        
        Algorithm: Floyd's build heap algorithm
        Start from last non-leaf node and heapify each node
        """
        self.operations_log.append(f"Building heap from {arr}")
        self.heap = arr.copy()
        n = len(self.heap)
        
        # Start from last non-leaf node
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(i)
        
        self.operations_log.append(f"Heap built: {self.heap}")
        return self
    
    def _heapify(self, i):
        """
        Heapify subtree rooted at index i (recursive version)
        """
        n = len(self.heap)
        extreme = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        # Find extreme among node and children
        if left < n and self.compare(self.heap[left], self.heap[extreme]):
            extreme = left
        
        if right < n and self.compare(self.heap[right], self.heap[extreme]):
            extreme = right
        
        # If heap property violated, swap and recursively heapify
        if extreme != i:
            self.swap(i, extreme)
            self._heapify(extreme)
    
    # ========== UTILITY FUNCTIONS ==========
    
    def peek(self):
        """Return root without removing it"""
        return self.heap[0] if self.heap else None
    
    def size(self):
        """Return number of elements"""
        return len(self.heap)
    
    def is_empty(self):
        """Check if heap is empty"""
        return len(self.heap) == 0
    
    def clear(self):
        """Clear the heap"""
        self.heap = []
        self.comparisons = 0
        self.swaps = 0
        self.operations_log = []
        return self
    
    def get_stats(self):
        """Get operation statistics"""
        return {
            'size': len(self.heap),
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'operations': len(self.operations_log)
        }
    
    def __str__(self):
        return str(self.heap)
    
    def __len__(self):
        return len(self.heap)


class MaxHeap(Heap):
    """Max Heap Implementation"""
    
    def __init__(self):
        super().__init__('max')
    
    def insert(self, value):
        """Insert value into max heap"""
        return super().insert(value)
    
    def extract_max(self):
        """Extract maximum value"""
        return self.extract_root()
    
    def get_max(self):
        """Get maximum value without removing"""
        return self.peek()
    
    def heap_sort(self, arr=None):
        """
        Heap sort algorithm
        Returns sorted array in ascending order
        """
        if arr is not None:
            self.build_heap(arr)
        
        n = len(self.heap)
        sorted_arr = []
        original_heap = self.heap.copy()
        
        for _ in range(n):
            sorted_arr.append(self.extract_max())
        
        # Restore heap
        self.heap = original_heap
        return sorted_arr


class MinHeap(Heap):
    """Min Heap Implementation"""
    
    def __init__(self):
        super().__init__('min')
    
    def insert(self, value):
        """Insert value into min heap"""
        return super().insert(value)
    
    def extract_min(self):
        """Extract minimum value"""
        return self.extract_root()
    
    def get_min(self):
        """Get minimum value without removing"""
        return self.peek()
    
    def heap_sort(self, arr=None):
        """
        Heap sort algorithm
        Returns sorted array in descending order
        """
        if arr is not None:
            self.build_heap(arr)
        
        n = len(self.heap)
        sorted_arr = []
        original_heap = self.heap.copy()
        
        for _ in range(n):
            sorted_arr.append(self.extract_min())
        
        # Restore heap
        self.heap = original_heap
        return sorted_arr


class PriorityQueue:
    """Priority Queue implementation using heap"""
    
    def __init__(self, priority_type='max'):
        """
        Initialize priority queue
        Args:
            priority_type: 'max' for highest priority first, 'min' for lowest priority first
        """
        self.heap = MaxHeap() if priority_type == 'max' else MinHeap()
        self.priority_type = priority_type
    
    def enqueue(self, item, priority):
        """Add item with given priority"""
        self.heap.insert((priority, item))
        return self
    
    def dequeue(self):
        """Remove and return highest priority item"""
        item = self.heap.extract_root()
        if item:
            return item[1]  # Return the item, not the priority
        return None
    
    def peek(self):
        """View highest priority item without removing"""
        item = self.heap.peek()
        if item:
            return item[1]
        return None
    
    def is_empty(self):
        """Check if queue is empty"""
        return self.heap.is_empty()
    
    def size(self):
        """Get queue size"""
        return self.heap.size()
    
    def get_all_items(self):
        """Get all items with their priorities"""
        items = []
        for item in self.heap.heap:
            items.append((item[1], item[0]))  # (item, priority)
        # Sort by priority
        items.sort(key=lambda x: x[1], reverse=(self.priority_type == 'max'))
        return items


# ============================================================================
# HEAP SORT IMPLEMENTATION
# ============================================================================

class HeapSort:
    """Heap Sort Algorithm Implementation"""
    
    @staticmethod
    def sort(arr, ascending=True):
        """
        Sort array using heap sort
        Time Complexity: O(n log n)
        Space Complexity: O(1) - in-place sorting
        """
        n = len(arr)
        comparisons = 0
        swaps = 0
        
        def heapify(arr, n, i):
            nonlocal comparisons, swaps
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n:
                comparisons += 1
                if (ascending and arr[left] > arr[largest]) or (not ascending and arr[left] < arr[largest]):
                    largest = left
            
            if right < n:
                comparisons += 1
                if (ascending and arr[right] > arr[largest]) or (not ascending and arr[right] < arr[largest]):
                    largest = right
            
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                swaps += 1
                heapify(arr, n, largest)
        
        # Build heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
        
        # Extract elements
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            swaps += 1
            heapify(arr, i, 0, ascending)
        
        return arr, comparisons, swaps
    
    @staticmethod
    def sort_with_steps(arr, ascending=True):
        """
        Sort array with step-by-step tracking
        Returns: (sorted_array, steps_list, comparisons, swaps)
        """
        steps = []
        n = len(arr)
        comparisons = 0
        swaps = 0
        
        steps.append(f"Original array: {arr}")
        
        def heapify(arr, n, i):
            nonlocal comparisons, swaps
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n:
                comparisons += 1
                if (ascending and arr[left] > arr[largest]) or (not ascending and arr[left] < arr[largest]):
                    largest = left
            
            if right < n:
                comparisons += 1
                if (ascending and arr[right] > arr[largest]) or (not ascending and arr[right] < arr[largest]):
                    largest = right
            
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                swaps += 1
                steps.append(f"  Swapped {arr[i]} and {arr[largest]}: {arr}")
                heapify(arr, n, largest)
        
        # Build heap
        steps.append(f"Building {'max' if ascending else 'min'} heap:")
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)
        
        steps.append(f"Heap built: {arr}")
        steps.append("\nExtracting elements:")
        
        # Extract elements
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            swaps += 1
            steps.append(f"  Moved root to position {i}: {arr}")
            heapify(arr, i, 0)
        
        if not ascending:
            arr.reverse()
            steps.append(f"Reversed for descending order: {arr}")
        
        return arr, steps, comparisons, swaps


# ============================================================================
# HEAP VISUALIZATION AND GUI
# ============================================================================

class HeapVisualizer:
    """Helper class for heap visualization"""
    
    @staticmethod
    def get_tree_representation(heap):
        """Get tree-like string representation"""
        if not heap:
            return "Empty heap"
        
        result = []
        n = len(heap)
        height = 0
        while (1 << height) - 1 < n:
            height += 1
        
        for level in range(height):
            level_start = (1 << level) - 1
            level_end = min((1 << (level + 1)) - 1, n)
            
            if level_start >= n:
                break
            
            level_nodes = heap[level_start:level_end]
            indent = " " * (height - level) * 3
            result.append(indent + "   ".join(map(str, level_nodes)))
        
        return "\n".join(result)
    
    @staticmethod
    def get_array_representation(heap):
        """Get array representation with indices"""
        result = []
        for i, val in enumerate(heap):
            result.append(f"[{i}]: {val}")
        return "\n".join(result)
    
    @staticmethod
    def get_heap_properties(heap):
        """Get heap properties as string"""
        if not heap:
            return "Heap is empty"
        
        props = []
        props.append(f"Size: {len(heap)}")
        props.append(f"Height: {int(math.log2(len(heap)) + 1)}")
        props.append(f"Root: {heap[0]}")
        
        # Check if valid heap
        is_valid = True
        n = len(heap)
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and heap[i] < heap[left]:
                is_valid = False
                break
            if right < n and heap[i] < heap[right]:
                is_valid = False
                break
        
        props.append(f"Valid Max Heap: {is_valid}")
        return "\n".join(props)


# ============================================================================
# MAIN GUI APPLICATION
# ============================================================================

class HeapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Complete Heap Data Structure & Algorithms")
        self.root.geometry("1400x800")
        
        # Initialize heaps
        self.max_heap = MaxHeap()
        self.min_heap = MinHeap()
        self.current_heap = self.max_heap
        self.current_heap_type = "max"
        
        # Priority queue
        self.priority_queue = PriorityQueue('max')
        self.processed_tasks = []
        
        # Colors
        self.setup_colors()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        
    def setup_colors(self):
        """Setup color scheme"""
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4CAF50"
        self.secondary_color = "#2196F3"
        self.text_color = "#333333"
        self.max_heap_color = "#FF6B6B"
        self.min_heap_color = "#6B5B95"
        self.highlight_color = "#FFD93D"
        
        self.root.configure(bg=self.bg_color)
    
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground=self.text_color)
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground=self.text_color)
        style.configure('Action.TButton', font=('Arial', 10), padding=5)
        style.configure('Success.TButton', font=('Arial', 10), background=self.primary_color)
        style.configure('Example.TButton', font=('Arial', 9), padding=3)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_heap_operations_tab()
        self.create_heap_sort_tab()
        self.create_priority_queue_tab()
        self.create_visualization_tab()
        self.create_examples_tab()
        self.create_comparison_tab()
        self.create_analysis_tab()
    
    def create_heap_operations_tab(self):
        """Tab for basic heap operations"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Heap Operations")
        
        # Control frame
        control_frame = ttk.LabelFrame(tab, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Heap type selection
        type_frame = ttk.Frame(control_frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(type_frame, text="Heap Type:").pack(side=tk.LEFT, padx=5)
        self.heap_type_var = tk.StringVar(value="max")
        ttk.Radiobutton(type_frame, text="Max Heap", variable=self.heap_type_var,
                       value="max", command=self.switch_heap).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="Min Heap", variable=self.heap_type_var,
                       value="min", command=self.switch_heap).pack(side=tk.LEFT, padx=5)
        
        # Input frame
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Value:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=10)
        self.value_entry.pack(side=tk.LEFT, padx=5)
        self.value_entry.bind('<Return>', lambda e: self.insert_value())
        
        ttk.Button(input_frame, text="Insert", command=self.insert_value,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Extract", command=self.extract_root,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Peek", command=self.peek_root,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        # Array input frame
        array_frame = ttk.Frame(control_frame)
        array_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(array_frame, text="Array (comma-separated):").pack(side=tk.LEFT, padx=5)
        self.array_entry = ttk.Entry(array_frame, width=30)
        self.array_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(array_frame, text="Build Heap", command=self.build_heap,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        # Random generation
        random_frame = ttk.Frame(control_frame)
        random_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(random_frame, text="Size:").pack(side=tk.LEFT, padx=5)
        self.size_spinbox = ttk.Spinbox(random_frame, from_=1, to=20, width=5)
        self.size_spinbox.set(8)
        self.size_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(random_frame, text="Generate Random", command=self.generate_random,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(random_frame, text="Clear", command=self.clear_heap,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        # Display frame
        display_frame = ttk.Frame(tab)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Left side - Tree representation
        tree_frame = ttk.LabelFrame(display_frame, text="Tree Representation", padding="10")
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.tree_text = scrolledtext.ScrolledText(tree_frame, height=20, font=('Courier', 10))
        self.tree_text.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Array representation and stats
        right_frame = ttk.Frame(display_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Array representation
        array_display_frame = ttk.LabelFrame(right_frame, text="Array Representation", padding="10")
        array_display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.array_listbox = tk.Listbox(array_display_frame, height=10, font=('Courier', 11))
        self.array_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Statistics
        stats_frame = ttk.LabelFrame(right_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.size_label = ttk.Label(stats_frame, text="Size: 0", style='Heading.TLabel')
        self.size_label.pack(anchor=tk.W, pady=2)
        
        self.root_label = ttk.Label(stats_frame, text="Root: None", style='Heading.TLabel')
        self.root_label.pack(anchor=tk.W, pady=2)
        
        self.comparisons_label = ttk.Label(stats_frame, text="Comparisons: 0", style='Heading.TLabel')
        self.comparisons_label.pack(anchor=tk.W, pady=2)
        
        self.swaps_label = ttk.Label(stats_frame, text="Swaps: 0", style='Heading.TLabel')
        self.swaps_label.pack(anchor=tk.W, pady=2)
    
    def create_heap_sort_tab(self):
        """Tab for heap sort operations"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Heap Sort")
        
        # Control frame
        control_frame = ttk.LabelFrame(tab, text="Sort Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Input frame
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Array:").pack(side=tk.LEFT, padx=5)
        self.sort_array_entry = ttk.Entry(input_frame, width=40)
        self.sort_array_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Sort Ascending", 
                  command=lambda: self.perform_sort(True),
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Sort Descending", 
                  command=lambda: self.perform_sort(False),
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        # Examples frame
        example_frame = ttk.Frame(control_frame)
        example_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(example_frame, text="Examples:").pack(side=tk.LEFT, padx=5)
        ttk.Button(example_frame, text="Random", 
                  command=lambda: self.load_sort_example("random"),
                  style='Example.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(example_frame, text="Sorted", 
                  command=lambda: self.load_sort_example("sorted"),
                  style='Example.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(example_frame, text="Reverse", 
                  command=lambda: self.load_sort_example("reverse"),
                  style='Example.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(example_frame, text="Duplicates", 
                  command=lambda: self.load_sort_example("duplicates"),
                  style='Example.TButton').pack(side=tk.LEFT, padx=2)
        
        # Display frame
        display_frame = ttk.Frame(tab)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Original array
        original_frame = ttk.LabelFrame(display_frame, text="Original Array", padding="10")
        original_frame.pack(fill=tk.X, pady=5)
        
        self.original_text = scrolledtext.ScrolledText(original_frame, height=2, font=('Courier', 11))
        self.original_text.pack(fill=tk.X)
        
        # Sorted array
        sorted_frame = ttk.LabelFrame(display_frame, text="Sorted Array", padding="10")
        sorted_frame.pack(fill=tk.X, pady=5)
        
        self.sorted_text = scrolledtext.ScrolledText(sorted_frame, height=2, font=('Courier', 11))
        self.sorted_text.pack(fill=tk.X)
        
        # Steps
        steps_frame = ttk.LabelFrame(display_frame, text="Sorting Steps", padding="10")
        steps_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.steps_text = scrolledtext.ScrolledText(steps_frame, height=15, font=('Courier', 10))
        self.steps_text.pack(fill=tk.BOTH, expand=True)
    
    def create_priority_queue_tab(self):
        """Tab for priority queue demonstration"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Priority Queue")
        
        # Control frame
        control_frame = ttk.LabelFrame(tab, text="Priority Queue Operations", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Queue type
        type_frame = ttk.Frame(control_frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(type_frame, text="Queue Type:").pack(side=tk.LEFT, padx=5)
        self.pq_type_var = tk.StringVar(value="max")
        ttk.Radiobutton(type_frame, text="Higher Priority First", variable=self.pq_type_var,
                       value="max", command=self.switch_pq).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="Lower Priority First", variable=self.pq_type_var,
                       value="min", command=self.switch_pq).pack(side=tk.LEFT, padx=5)
        
        # Input frame
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Task:").pack(side=tk.LEFT, padx=5)
        self.task_entry = ttk.Entry(input_frame, width=20)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(input_frame, text="Priority:").pack(side=tk.LEFT, padx=5)
        self.priority_spinbox = ttk.Spinbox(input_frame, from_=1, to=10, width=5)
        self.priority_spinbox.set(5)
        self.priority_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Add Task", command=self.add_task,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Process Next", command=self.process_task,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Process All", command=self.process_all,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        # Examples
        example_frame = ttk.Frame(control_frame)
        example_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(example_frame, text="Examples:").pack(side=tk.LEFT, padx=5)
        ttk.Button(example_frame, text="Emergency Room", 
                  command=self.load_er_example,
                  style='Example.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(example_frame, text="Task Scheduler", 
                  command=self.load_scheduler_example,
                  style='Example.TButton').pack(side=tk.LEFT, padx=2)
        
        # Display frame
        display_frame = ttk.Frame(tab)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Pending tasks
        pending_frame = ttk.LabelFrame(display_frame, text="Pending Tasks", padding="10")
        pending_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.pending_text = scrolledtext.ScrolledText(pending_frame, height=20, font=('Courier', 10))
        self.pending_text.pack(fill=tk.BOTH, expand=True)
        
        # Processed tasks
        processed_frame = ttk.LabelFrame(display_frame, text="Processed Tasks", padding="10")
        processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.processed_text = scrolledtext.ScrolledText(processed_frame, height=20, font=('Courier', 10))
        self.processed_text.pack(fill=tk.BOTH, expand=True)
    
    def create_visualization_tab(self):
        """Tab for heap visualization"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Visualization")
        
        # Control frame
        control_frame = ttk.LabelFrame(tab, text="Visualization Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Refresh", command=self.refresh_visualization,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Animate Extract", command=self.animate_extract,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        # Canvas
        self.vis_canvas = tk.Canvas(tab, bg='white', width=800, height=500)
        self.vis_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Info label
        self.vis_info_label = ttk.Label(tab, text="", style='Heading.TLabel')
        self.vis_info_label.pack(pady=5)
    
    def create_examples_tab(self):
        """Tab with heap examples"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Examples")
        
        # Examples frame
        examples_frame = ttk.Frame(tab)
        examples_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Example 1: Build heap
        example1 = ttk.LabelFrame(examples_frame, text="Build Heap from Array", padding="10")
        example1.pack(fill=tk.X, pady=5)
        
        ttk.Label(example1, text="Array: [4, 10, 3, 5, 1]").pack(anchor=tk.W)
        ttk.Button(example1, text="Build Max Heap", 
                  command=lambda: self.load_example([4, 10, 3, 5, 1], "max"),
                  style='Example.TButton').pack(anchor=tk.W, pady=2)
        ttk.Button(example1, text="Build Min Heap", 
                  command=lambda: self.load_example([4, 10, 3, 5, 1], "min"),
                  style='Example.TButton').pack(anchor=tk.W, pady=2)
        
        # Example 2: Insert operations
        example2 = ttk.LabelFrame(examples_frame, text="Sequential Insertions", padding="10")
        example2.pack(fill=tk.X, pady=5)
        
        ttk.Label(example2, text="Insert: 5, 8, 3, 12, 9, 4").pack(anchor=tk.W)
        ttk.Button(example2, text="Show Steps", 
                  command=self.show_insert_steps,
                  style='Example.TButton').pack(anchor=tk.W, pady=2)
        
        # Example 3: Extract operations
        example3 = ttk.LabelFrame(examples_frame, text="Extract Operations", padding="10")
        example3.pack(fill=tk.X, pady=5)
        
        ttk.Label(example3, text="From heap [15, 10, 8, 7, 6, 5]").pack(anchor=tk.W)
        ttk.Button(example3, text="Show Steps", 
                  command=self.show_extract_steps,
                  style='Example.TButton').pack(anchor=tk.W, pady=2)
        
        # Example 4: Heapify process
        example4 = ttk.LabelFrame(examples_frame, text="Heapify Process", padding="10")
        example4.pack(fill=tk.X, pady=5)
        
        ttk.Label(example4, text="Array: [3, 5, 8, 10, 1, 7, 4]").pack(anchor=tk.W)
        ttk.Button(example4, text="Show Heapify", 
                  command=self.show_heapify_steps,
                  style='Example.TButton').pack(anchor=tk.W, pady=2)
    
    def create_comparison_tab(self):
        """Tab comparing max and min heaps"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Comparison")
        
        # Main frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left - Max Heap
        max_frame = ttk.LabelFrame(main_frame, text="Max Heap", padding="10")
        max_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(max_frame, text="Properties:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(max_frame, text="• Parent ≥ Children").pack(anchor=tk.W)
        ttk.Label(max_frame, text="• Maximum at root").pack(anchor=tk.W)
        ttk.Label(max_frame, text="• Used for: Higher priority first").pack(anchor=tk.W)
        ttk.Label(max_frame, text="• Heap sort: ascending order").pack(anchor=tk.W)
        
        ttk.Button(max_frame, text="Build Example", 
                  command=lambda: self.load_comparison_example("max"),
                  style='Example.TButton').pack(anchor=tk.W, pady=5)
        
        self.max_canvas = tk.Canvas(max_frame, bg='white', width=350, height=200)
        self.max_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Right - Min Heap
        min_frame = ttk.LabelFrame(main_frame, text="Min Heap", padding="10")
        min_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(min_frame, text="Properties:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(min_frame, text="• Parent ≤ Children").pack(anchor=tk.W)
        ttk.Label(min_frame, text="• Minimum at root").pack(anchor=tk.W)
        ttk.Label(min_frame, text="• Used for: Lower priority first").pack(anchor=tk.W)
        ttk.Label(min_frame, text="• Heap sort: descending order").pack(anchor=tk.W)
        
        ttk.Button(min_frame, text="Build Example", 
                  command=lambda: self.load_comparison_example("min"),
                  style='Example.TButton').pack(anchor=tk.W, pady=5)
        
        self.min_canvas = tk.Canvas(min_frame, bg='white', width=350, height=200)
        self.min_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Complexity comparison
        complexity_frame = ttk.LabelFrame(tab, text="Time Complexity", padding="10")
        complexity_frame.pack(fill=tk.X, pady=5)
        
        columns = ('Operation', 'Max Heap', 'Min Heap')
        tree = ttk.Treeview(complexity_frame, columns=columns, show='headings', height=4)
        
        tree.heading('Operation', text='Operation')
        tree.heading('Max Heap', text='Max Heap')
        tree.heading('Min Heap', text='Min Heap')
        
        tree.insert('', 'end', values=('Insert', 'O(log n)', 'O(log n)'))
        tree.insert('', 'end', values=('Extract', 'O(log n)', 'O(log n)'))
        tree.insert('', 'end', values=('Peek', 'O(1)', 'O(1)'))
        tree.insert('', 'end', values=('Build Heap', 'O(n)', 'O(n)'))
        tree.insert('', 'end', values=('Heap Sort', 'O(n log n)', 'O(n log n)'))
        
        tree.pack()
    
    def create_analysis_tab(self):
        """Tab for heap analysis"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Analysis")
        
        # Control frame
        control_frame = ttk.LabelFrame(tab, text="Analysis Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Array Size:").pack(side=tk.LEFT, padx=5)
        self.analysis_size = ttk.Spinbox(control_frame, from_=10, to=1000, width=10)
        self.analysis_size.set(100)
        self.analysis_size.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Run Analysis", command=self.run_analysis,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(tab, text="Analysis Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.analysis_text = scrolledtext.ScrolledText(results_frame, height=25, font=('Courier', 10))
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
    
    # ========== HEAP OPERATIONS ==========
    
    def switch_heap(self):
        """Switch between max and min heap"""
        self.current_heap_type = self.heap_type_var.get()
        if self.current_heap_type == "max":
            self.current_heap = self.max_heap
        else:
            self.current_heap = self.min_heap
        self.update_display()
    
    def insert_value(self):
        """Insert value into heap"""
        try:
            value = int(self.value_entry.get())
            self.current_heap.insert(value)
            self.update_display()
            self.value_entry.delete(0, tk.END)
            self.vis_info_label.config(text=f"Inserted: {value}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
    
    def extract_root(self):
        """Extract root from heap"""
        if self.current_heap_type == "max":
            value = self.current_heap.extract_max()
        else:
            value = self.current_heap.extract_min()
        
        if value is not None:
            messagebox.showinfo("Extract", f"Extracted: {value}")
            self.vis_info_label.config(text=f"Extracted: {value}")
        else:
            messagebox.showwarning("Warning", "Heap is empty")
        
        self.update_display()
    
    def peek_root(self):
        """Peek at root value"""
        value = self.current_heap.peek()
        if value is not None:
            messagebox.showinfo("Peek", f"Current root: {value}")
        else:
            messagebox.showwarning("Warning", "Heap is empty")
    
    def build_heap(self):
        """Build heap from array"""
        try:
            array_str = self.array_entry.get()
            if array_str.strip():
                arr = [int(x.strip()) for x in array_str.split(',')]
                self.current_heap.build_heap(arr)
                self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")
    
    def generate_random(self):
        """Generate random heap"""
        try:
            size = int(self.size_spinbox.get())
            arr = [random.randint(1, 100) for _ in range(size)]
            self.current_heap.build_heap(arr)
            self.array_entry.delete(0, tk.END)
            self.array_entry.insert(0, ', '.join(map(str, arr)))
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid size")
    
    def clear_heap(self):
        """Clear the heap"""
        if self.current_heap_type == "max":
            self.max_heap = MaxHeap()
            self.current_heap = self.max_heap
        else:
            self.min_heap = MinHeap()
            self.current_heap = self.min_heap
        self.update_display()
    
    # ========== HEAP SORT OPERATIONS ==========
    
    def perform_sort(self, ascending):
        """Perform heap sort"""
        try:
            array_str = self.sort_array_entry.get()
            if not array_str.strip():
                messagebox.showwarning("Warning", "Please enter an array")
                return
            
            arr = [int(x.strip()) for x in array_str.split(',')]
            
            # Clear previous output
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, f"Original: {arr}")
            
            self.steps_text.delete(1.0, tk.END)
            
            # Perform sort with steps
            sorted_arr, steps, comparisons, swaps = HeapSort.sort_with_steps(arr.copy(), ascending)
            
            # Display steps
            for step in steps:
                self.steps_text.insert(tk.END, step + "\n")
            
            # Display result
            self.sorted_text.delete(1.0, tk.END)
            self.sorted_text.insert(1.0, f"Sorted: {sorted_arr}")
            
            # Show statistics
            self.steps_text.insert(tk.END, f"\n" + "="*50 + "\n")
            self.steps_text.insert(tk.END, f"Statistics:\n")
            self.steps_text.insert(tk.END, f"  Comparisons: {comparisons}\n")
            self.steps_text.insert(tk.END, f"  Swaps: {swaps}\n")
            self.steps_text.insert(tk.END, f"  Time Complexity: O(n log n)\n")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")
    
    def load_sort_example(self, example_type):
        """Load example for sorting"""
        examples = {
            "random": [random.randint(1, 100) for _ in range(8)],
            "sorted": [1, 2, 3, 4, 5, 6, 7, 8],
            "reverse": [8, 7, 6, 5, 4, 3, 2, 1],
            "duplicates": [5, 3, 8, 3, 1, 5, 2, 8]
        }
        
        arr = examples.get(example_type, examples["random"])
        self.sort_array_entry.delete(0, tk.END)
        self.sort_array_entry.insert(0, ', '.join(map(str, arr)))
    
    # ========== PRIORITY QUEUE OPERATIONS ==========
    
    def switch_pq(self):
        """Switch priority queue type"""
        self.priority_queue = PriorityQueue(self.pq_type_var.get())
        self.processed_tasks = []
        self.update_pq_display()
    
    def add_task(self):
        """Add task to priority queue"""
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task")
            return
        
        try:
            priority = int(self.priority_spinbox.get())
            self.priority_queue.enqueue(task, priority)
            self.update_pq_display()
            self.task_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid priority")
    
    def process_task(self):
        """Process next task"""
        task = self.priority_queue.dequeue()
        if task:
            self.processed_tasks.append((task, time.strftime("%H:%M:%S")))
            self.update_pq_display()
        else:
            messagebox.showwarning("Warning", "No tasks in queue")
    
    def process_all(self):
        """Process all tasks"""
        count = 0
        while not self.priority_queue.is_empty():
            task = self.priority_queue.dequeue()
            self.processed_tasks.append((task, time.strftime("%H:%M:%S")))
            count += 1
        
        if count > 0:
            messagebox.showinfo("Success", f"Processed {count} tasks")
            self.update_pq_display()
        else:
            messagebox.showwarning("Warning", "No tasks in queue")
    
    def load_er_example(self):
        """Load emergency room example"""
        self.switch_pq()
        tasks = [
            (10, "Cardiac Arrest"),
            (8, "Severe Bleeding"),
            (9, "Heart Attack"),
            (5, "Broken Leg"),
            (3, "Mild Fever"),
            (7, "Difficulty Breathing")
        ]
        for priority, task in tasks:
            self.priority_queue.enqueue(task, priority)
        self.update_pq_display()
    
    def load_scheduler_example(self):
        """Load task scheduler example"""
        self.switch_pq()
        tasks = [
            (1, "System Update"),
            (3, "User Request"),
            (2, "Background Process"),
            (5, "Critical Alert"),
            (4, "Data Backup")
        ]
        for priority, task in tasks:
            self.priority_queue.enqueue(task, priority)
        self.update_pq_display()
    
    def update_pq_display(self):
        """Update priority queue display"""
        # Update pending tasks
        self.pending_text.delete(1.0, tk.END)
        items = self.priority_queue.get_all_items()
        if items:
            self.pending_text.insert(tk.END, "Tasks (by priority):\n\n")
            for task, priority in items:
                self.pending_text.insert(tk.END, f"  • {task} (Priority: {priority})\n")
        else:
            self.pending_text.insert(tk.END, "No pending tasks")
        
        # Update processed tasks
        self.processed_text.delete(1.0, tk.END)
        if self.processed_tasks:
            self.processed_text.insert(tk.END, "Processed tasks:\n\n")
            for task, timestamp in reversed(self.processed_tasks[-10:]):
                self.processed_text.insert(tk.END, f"  • {task} at {timestamp}\n")
        else:
            self.processed_text.insert(tk.END, "No processed tasks")
    
    # ========== VISUALIZATION ==========
    
    def refresh_visualization(self):
        """Refresh heap visualization"""
        self.vis_canvas.delete("all")
        
        if not self.current_heap.heap:
            self.vis_canvas.create_text(400, 250, text="Heap is empty", 
                                        font=('Arial', 16), fill='gray')
            return
        
        self.draw_heap(self.vis_canvas, self.current_heap.heap, 
                      self.current_heap_type == "max")
    
    def draw_heap(self, canvas, heap, is_max_heap):
        """Draw heap tree visualization"""
        if not heap:
            return
        
        n = len(heap)
        height = self.get_tree_height(n)
        
        # Starting position
        start_x = 400
        start_y = 50
        level_height = 80
        
        # Draw nodes
        nodes = [(0, start_x, start_y)]
        drawn = {0}
        
        while nodes:
            idx, x, y = nodes.pop(0)
            
            # Calculate spacing
            level = self.get_level(idx)
            width_factor = 2 ** (height - level - 1)
            spacing = 40 * width_factor
            
            # Draw connections
            left_idx = 2 * idx + 1
            right_idx = 2 * idx + 2
            
            if left_idx < n:
                left_x = x - spacing
                left_y = y + level_height
                canvas.create_line(x, y + 15, left_x, left_y - 15, 
                                 fill='gray', width=2, dash=(4, 2))
                if left_idx not in drawn:
                    nodes.append((left_idx, left_x, left_y))
                    drawn.add(left_idx)
            
            if right_idx < n:
                right_x = x + spacing
                right_y = y + level_height
                canvas.create_line(x, y + 15, right_x, right_y - 15, 
                                 fill='gray', width=2, dash=(4, 2))
                if right_idx not in drawn:
                    nodes.append((right_idx, right_x, right_y))
                    drawn.add(right_idx)
            
            # Draw node
            color = self.max_heap_color if is_max_heap else self.min_heap_color
            canvas.create_oval(x-20, y-15, x+20, y+15, fill=color, 
                             outline='darkred' if is_max_heap else 'darkblue', width=2)
            canvas.create_text(x, y, text=str(heap[idx]), 
                             font=('Arial', 12, 'bold'), fill='white')
            
            # Add index
            canvas.create_text(x, y-25, text=f"[{idx}]", 
                             font=('Arial', 8), fill='gray')
    
    def get_tree_height(self, n):
        """Calculate tree height"""
        height = 0
        while (2 ** height) - 1 < n:
            height += 1
        return height
    
    def get_level(self, index):
        """Get level of node"""
        level = 0
        while index > 0:
            index = (index - 1) // 2
            level += 1
        return level
    
    def animate_insert(self):
        """Animate insert operation"""
        if not self.value_entry.get():
            messagebox.showwarning("Warning", "Please enter a value")
            return
        
        try:
            value = int(self.value_entry.get())
            self.current_heap.insert(value)
            self.refresh_visualization()
            self.vis_info_label.config(text=f"Inserted: {value}")
            self.update_display()
            self.value_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
    
    def animate_extract(self):
        """Animate extract operation"""
        if self.current_heap_type == "max":
            value = self.current_heap.extract_max()
        else:
            value = self.current_heap.extract_min()
        
        if value is not None:
            self.refresh_visualization()
            self.vis_info_label.config(text=f"Extracted: {value}")
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Heap is empty")
    
    # ========== EXAMPLES ==========
    
    def load_example(self, arr, heap_type):
        """Load example heap"""
        self.heap_type_var.set(heap_type)
        self.switch_heap()
        self.current_heap.build_heap(arr)
        self.array_entry.delete(0, tk.END)
        self.array_entry.insert(0, ', '.join(map(str, arr)))
        self.update_display()
        self.notebook.select(0)
    
    def show_insert_steps(self):
        """Show insert operation steps"""
        values = [5, 8, 3, 12, 9, 4]
        heap = MaxHeap()
        steps = []
        
        for val in values:
            heap.insert(val)
            steps.append(f"After inserting {val}: {heap.heap}")
        
        messagebox.showinfo("Insert Steps", "\n".join(steps))
        self.current_heap = heap
        self.update_display()
    
    def show_extract_steps(self):
        """Show extract operation steps"""
        initial = [15, 10, 8, 7, 6, 5]
        heap = MaxHeap()
        heap.build_heap(initial)
        
        steps = [f"Initial heap: {heap.heap}"]
        extracted = []
        
        for i in range(3):
            val = heap.extract_max()
            extracted.append(val)
            steps.append(f"Extracted {val}, heap: {heap.heap}")
        
        steps.append(f"Extracted values: {extracted}")
        messagebox.showinfo("Extract Steps", "\n".join(steps))
        
        self.current_heap = heap
        self.update_display()
    
    def show_heapify_steps(self):
        """Show heapify process"""
        arr = [3, 5, 8, 10, 1, 7, 4]
        heap = MaxHeap()
        
        steps = [f"Original: {arr}"]
        heap.heap = arr.copy()
        
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heap._heapify(i)
            steps.append(f"After heapifying index {i}: {heap.heap}")
        
        messagebox.showinfo("Heapify Steps", "\n".join(steps))
        self.current_heap = heap
        self.update_display()
    
    def load_comparison_example(self, heap_type):
        """Load comparison example"""
        if heap_type == "max":
            arr = [1, 3, 5, 7, 9, 2, 4, 6, 8]
            heap = MaxHeap()
            heap.build_heap(arr)
            self.max_canvas.delete("all")
            self.draw_heap(self.max_canvas, heap.heap, True)
            self.max_canvas.create_text(175, 20, text=f"Root: {heap.peek()}", 
                                       font=('Arial', 10, 'bold'), fill='darkred')
        else:
            arr = [9, 8, 7, 6, 5, 4, 3, 2, 1]
            heap = MinHeap()
            heap.build_heap(arr)
            self.min_canvas.delete("all")
            self.draw_heap(self.min_canvas, heap.heap, False)
            self.min_canvas.create_text(175, 20, text=f"Root: {heap.peek()}", 
                                       font=('Arial', 10, 'bold'), fill='darkblue')
    
    # ========== ANALYSIS ==========
    
    def run_analysis(self):
        """Run heap analysis"""
        try:
            size = int(self.analysis_size.get())
            
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, "HEAP PERFORMANCE ANALYSIS\n")
            self.analysis_text.insert(tk.END, "="*60 + "\n\n")
            
            # Test with random arrays
            for test_size in [10, 50, 100, 500, 1000]:
                if test_size > size:
                    continue
                    
                self.analysis_text.insert(tk.END, f"\nTesting with {test_size} elements:\n")
                self.analysis_text.insert(tk.END, "-"*40 + "\n")
                
                # Generate random array
                arr = [random.randint(1, 1000) for _ in range(test_size)]
                
                # Test Max Heap build
                heap = MaxHeap()
                start_time = time.time()
                heap.build_heap(arr)
                build_time = time.time() - start_time
                
                self.analysis_text.insert(tk.END, 
                    f"Build Heap: {build_time:.6f} seconds, "
                    f"Comparisons: {heap.comparisons}, "
                    f"Swaps: {heap.swaps}\n")
                
                # Test insertions
                heap = MaxHeap()
                start_time = time.time()
                comparisons = 0
                swaps = 0
                for val in arr[:10]:  # Insert first 10 elements
                    heap.insert(val)
                    comparisons += heap.comparisons
                    swaps += heap.swaps
                insert_time = time.time() - start_time
                
                self.analysis_text.insert(tk.END, 
                    f"Insert 10 elements: {insert_time:.6f} seconds, "
                    f"Avg comparisons: {comparisons//10}, "
                    f"Avg swaps: {swaps//10}\n")
                
                # Test heap sort
                start_time = time.time()
                sorted_arr, sort_comparisons, sort_swaps = HeapSort.sort(arr.copy(), True)
                sort_time = time.time() - start_time
                
                self.analysis_text.insert(tk.END, 
                    f"Heap Sort: {sort_time:.6f} seconds, "
                    f"Comparisons: {sort_comparisons}, "
                    f"Swaps: {sort_swaps}\n")
            
            # Add complexity analysis
            self.analysis_text.insert(tk.END, "\n\n" + "="*60 + "\n")
            self.analysis_text.insert(tk.END, "TIME COMPLEXITY ANALYSIS\n")
            self.analysis_text.insert(tk.END, "="*60 + "\n\n")
            
            self.analysis_text.insert(tk.END, "Operation    | Best Case  | Average Case | Worst Case\n")
            self.analysis_text.insert(tk.END, "-"*60 + "\n")
            self.analysis_text.insert(tk.END, "Insert       | O(1)       | O(log n)     | O(log n)\n")
            self.analysis_text.insert(tk.END, "Extract      | O(log n)   | O(log n)     | O(log n)\n")
            self.analysis_text.insert(tk.END, "Build Heap   | O(n)       | O(n)         | O(n)\n")
            self.analysis_text.insert(tk.END, "Heap Sort    | O(n log n) | O(n log n)   | O(n log n)\n")
            self.analysis_text.insert(tk.END, "Peek         | O(1)       | O(1)         | O(1)\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    # ========== DISPLAY UPDATE ==========
    
    def update_display(self):
        """Update all displays"""
        # Update listbox
        self.array_listbox.delete(0, tk.END)
        for i, val in enumerate(self.current_heap.heap):
            self.array_listbox.insert(tk.END, f"[{i}]: {val}")
        
        # Update tree text
        self.tree_text.delete(1.0, tk.END)
        if self.current_heap.heap:
            self.tree_text.insert(tk.END, 
                HeapVisualizer.get_tree_representation(self.current_heap.heap))
        else:
            self.tree_text.insert(tk.END, "Heap is empty")
        
        # Update statistics
        self.size_label.config(text=f"Size: {self.current_heap.size()}")
        
        root_val = self.current_heap.peek()
        if root_val is not None:
            if self.current_heap_type == "max":
                self.root_label.config(text=f"Max: {root_val}")
            else:
                self.root_label.config(text=f"Min: {root_val}")
        else:
            self.root_label.config(text="Root: None")
        
        stats = self.current_heap.get_stats()
        self.comparisons_label.config(text=f"Comparisons: {stats['comparisons']}")
        self.swaps_label.config(text=f"Swaps: {stats['swaps']}")
        
        # Refresh visualization if on that tab
        if self.notebook.index(self.notebook.select()) == 3:
            self.refresh_visualization()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = HeapGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()