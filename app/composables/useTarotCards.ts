import { createSharedComposable } from '@vueuse/core'
import type { Card } from '#shared/types/tarot'

const _useTarotCards = () => {
  const toast = useToast()

  // State
  const cards = ref<Card[]>([])
  const selectedCardIndex = ref<number | null>(null)
  const searchQuery = ref('')
  const isSaving = ref(false)
  const isImportModal = ref(false)
  const importJson = ref('')
  const isHotspotEditorOpen = ref(false)

  // Options
  const suitOptions = [
    { label: '大阿卡那', value: 'major' },
    { label: '权杖', value: 'wands' },
    { label: '金币', value: 'pentacles' },
    { label: '圣杯', value: 'cups' },
    { label: '宝剑', value: 'swords' }
  ]

  const detailTypeOptions = [
    { label: '视觉描述', value: 'visual' },
    { label: '象征意义', value: 'symbolism' },
    { label: '解释', value: 'interpretation' }
  ]

  // Computed
  const selectedCard = computed(() => {
    if (selectedCardIndex.value !== null) {
      return cards.value[selectedCardIndex.value]
    }
    return null
  })

  const filteredCards = computed(() => {
    if (!searchQuery.value) return cards.value
    const query = searchQuery.value.toLowerCase()
    return cards.value.filter(
      card => card.label.toLowerCase().includes(query) || card.suit.toLowerCase().includes(query)
    )
  })

  // Methods
  const createEmptyCard = (): Card => ({
    suit: 'major',
    label: '新牌',
    elements: [],
    image: '',
    image3d: '',
    meanings: {
      upright: {
        meaning: '',
        keywords: [],
        summary: '',
        scenarios: []
      },
      reversed: {
        meaning: '',
        keywords: [],
        summary: '',
        scenarios: []
      }
    }
  })

  const initializeCards = async () => {
    try {
      const data = await $fetch('/api/data.json')
      if (Array.isArray(data) && data.length > 0) {
        cards.value = data
      } else {
        // 初始化 78 张空牌
        cards.value = Array(78).fill(null).map((_, i) => ({
          ...createEmptyCard(),
          label: `牌 ${i + 1}`
        }))
      }
      if (cards.value.length > 0) {
        selectedCardIndex.value = 0
      }
    } catch (err) {
      console.error('Failed to load cards:', err)
      // 初始化默认数据
      cards.value = Array(78).fill(null).map((_, i) => ({
        ...createEmptyCard(),
        label: `牌 ${i + 1}`
      }))
      if (cards.value.length > 0) {
        selectedCardIndex.value = 0
      }
    }
  }

  const addElement = () => {
    if (selectedCard.value) {
      selectedCard.value.elements.push({
        label: '新元素',
        x: 0,
        y: 0,
        r: 0,
        details: []
      })
    }
  }

  const removeElement = (index: number) => {
    if (selectedCard.value) {
      selectedCard.value.elements.splice(index, 1)
    }
  }

  const addDetail = (elementIndex: number) => {
    if (selectedCard.value) {
      selectedCard.value.elements[elementIndex]!.details.push({
        type: 'visual',
        content: ''
      })
    }
  }

  const removeDetail = (elementIndex: number, detailIndex: number) => {
    if (selectedCard.value) {
      selectedCard.value.elements[elementIndex]!.details.splice(detailIndex, 1)
    }
  }

  const saveData = async () => {
    if (window.confirm('确定要保存所有牌的数据吗？该操作会使用当前工作区的的数据覆盖服务器上的数据。')) {
      isSaving.value = true
      try {
        await $fetch('/api/data', {
          method: 'POST',
          body: { data: cards.value }
        })
        toast.add({
          title: '保存成功',
          description: '所有牌数据已保存'
        })
      } catch (err) {
        console.error('Failed to save:', err)
        toast.add({
          title: '保存失败',
          description: '保存数据时出错'
        })
      } finally {
        isSaving.value = false
      }
    }
  }

  const saveCurrentCard = async () => {
    if (selectedCardIndex.value === null || !selectedCard.value) return

    isSaving.value = true
    try {
      await $fetch('/api/data/update', {
        method: 'POST',
        body: {
          index: selectedCardIndex.value,
          card: selectedCard.value
        }
      })
      toast.add({
        title: '保存成功',
        description: `已保存 ${selectedCard.value.label}`
      })
    } catch (err) {
      console.error('Failed to save card:', err)
      toast.add({
        title: '保存失败',
        description: '保存单张牌时出错'
      })
    } finally {
      isSaving.value = false
    }
  }

  const exportData = () => {
    const json = JSON.stringify(cards.value, null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `tarot-cards-${new Date().getTime()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const importData = () => {
    try {
      const imported = JSON.parse(importJson.value)
      if (Array.isArray(imported)) {
        cards.value = imported
        selectedCardIndex.value = 0
        isImportModal.value = false
        importJson.value = ''
        toast.add({
          title: '导入成功',
          description: `已导入 ${imported.length} 张牌`
        })
      }
    } catch (err) {
      console.error('Import error:', err)
      toast.add({
        title: '导入失败',
        description: 'JSON 格式无效'
      })
    }
  }

  return {
    // State
    cards,
    selectedCardIndex,
    searchQuery,
    isSaving,
    isImportModal,
    importJson,
    isHotspotEditorOpen,

    // Options
    suitOptions,
    detailTypeOptions,

    // Computed
    selectedCard,
    filteredCards,

    // Methods
    createEmptyCard,
    initializeCards,
    addElement,
    removeElement,
    addDetail,
    removeDetail,
    saveData,
    saveCurrentCard,
    exportData,
    importData
  }
}

// 使用 createSharedComposable 创建全局共享的 composable
export const useTarotCards = createSharedComposable(_useTarotCards)
