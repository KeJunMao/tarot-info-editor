<template>
  <div
    ref="containerRef"
    class="relative   overflow-hidden select-none  mx-auto"
    style="width: 350px; height: 560px;"
    @mousemove="onMouseMove"
    @mouseup="onMouseUp"
    @mouseleave="onMouseUp"
  >
    <img
      v-if="imageUrl"
      :src="imageUrl"
      class="w-full h-full object-fill pointer-events-none"
      draggable="false"
      alt="Card Image"
    >
    <div
      v-else
      class="flex items-center justify-center w-full h-full text-gray-400"
    >
      无图片
    </div>

    <!-- Elements -->
    <div
      v-for="(element, index) in elements"
      :key="index"
      class="absolute rounded-full border-2 cursor-move group flex items-center justify-center box-border"
      :class="[
        selectedIndex === index
          ? 'border-primary-500 bg-primary-500/10 z-20'
          : 'border-yellow-400 bg-yellow-400/10 z-10 hover:border-yellow-500'
      ]"
      :style="{
        left: `${element.x}px`,
        top: `${element.y}px`,
        width: `${Math.max(20, element.r * 2)}px`,
        height: `${Math.max(20, element.r * 2)}px`
      }"
      @mousedown.stop="onDragStart($event, index)"
    >
      <!-- Label tooltip -->
      <div class="hidden group-hover:block absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900/80 text-white text-xs px-2 py-1 rounded whitespace-nowrap z-50 pointer-events-none">
        {{ element.label }}
      </div>

      <!-- Resize Handle (Bottom-Right) -->
      <div
        v-if="selectedIndex === index"
        class="absolute w-4 h-4 bg-primary-600 rounded-full cursor-se-resize flex items-center justify-center shadow-sm z-30 ring-2 ring-white dark:ring-gray-900"
        style="bottom: 0; right: 0; transform: translate(40%, 40%);"
        @mousedown.stop="onResizeStart($event, index)"
      >
        <UIcon
          name="i-lucide-scaling"
          class="text-white w-2.5 h-2.5"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Element } from '#shared/types/tarot'

const props = defineProps<{
  imageUrl: string
  elements: Element[]
}>()

const selectedIndex = ref<number | null>(null)
const containerRef = ref<HTMLElement | null>(null)

// Dragging State
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })
// Resizing State
const isResizing = ref(false)
// Common State
const activeIndex = ref<number | null>(null)

function onDragStart(e: MouseEvent, index: number) {
  if (!containerRef.value) return

  selectedIndex.value = index
  activeIndex.value = index
  isDragging.value = true

  const el = props.elements[index]
  const containerRect = containerRef.value.getBoundingClientRect()
  if (!el) return

  // Calculate offset from the top-left corner of the element global coordinates
  const elementGlobalX = containerRect.left + el.x
  const elementGlobalY = containerRect.top + el.y

  dragOffset.value = {
    x: e.clientX - elementGlobalX,
    y: e.clientY - elementGlobalY
  }
}

function onResizeStart(e: MouseEvent, index: number) {
  selectedIndex.value = index
  activeIndex.value = index
  isResizing.value = true
}

function onMouseMove(e: MouseEvent) {
  if (activeIndex.value === null) return
  if (!containerRef.value) return

  const element = props.elements[activeIndex.value]
  if (!element) return
  const containerRect = containerRef.value.getBoundingClientRect()

  if (isDragging.value) {
    // element.x = (MouseGlobalX - OffsetX) - ContainerLeft
    element.x = Math.round(e.clientX - dragOffset.value.x - containerRect.left)
    element.y = Math.round(e.clientY - dragOffset.value.y - containerRect.top)
  } else if (isResizing.value) {
    // Mouse relative to container
    const mouseXInContainer = e.clientX - containerRect.left
    const mouseYInContainer = e.clientY - containerRect.top

    // Width = MouseX - ElementX
    // Height = MouseY - ElementY
    // We base it roughly on the dist to make it feel like dragging the corner
    const newWidth = mouseXInContainer - element.x
    const newHeight = mouseYInContainer - element.y

    // Ensure minimum size
    const size = Math.max(10, Math.max(newWidth, newHeight))

    element.r = Math.round(size / 2)
  }
}

function onMouseUp() {
  isDragging.value = false
  isResizing.value = false
  activeIndex.value = null
}
</script>
