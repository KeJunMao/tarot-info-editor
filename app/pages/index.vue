<template>
  <div>
    <UContainer>
      <UPage>
        <UPageHeader
          title="塔罗牌编辑器"
        >
          <template #links>
            <UButton
              icon="i-lucide-upload"
              variant="outline"
              @click="isImportModal = true"
            >
              导入
            </UButton>
            <UButton
              icon="i-lucide-download"
              variant="outline"
              @click="exportData"
            >
              导出
            </UButton>
            <UButton
              icon="i-lucide-save"
              :loading="isSaving"
              @click="saveData"
            >
              保存所有数据
            </UButton>
          </template>
        </UPageHeader>
        <template #left>
          <UPageAside>
            <template #top>
              <UInput
                v-model="searchQuery"
                placeholder="搜索牌..."
                icon="i-lucide-search"
                class="mb-4"
              />
            </template>
            <UNavigationMenu
              orientation="vertical"
              :items="filteredCards.map((card, index) => {
                return {
                  label: card.label,
                  badge: card.suit,
                  active: selectedCardIndex === index,
                  onSelect: () => {
                    selectedCardIndex = index
                  }
                }
              })"
            />
          </UPageAside>
        </template>
        <UPageBody>
          <div
            v-if="selectedCard"
            class="space-y-6"
          >
            <!-- 基本信息 -->
            <UCard>
              <template #header>
                <h3 class="text-lg font-semibold">
                  基本信息
                </h3>
              </template>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <UFormField
                  label="牌名"
                  required
                >
                  <UInput
                    v-model="selectedCard.label"
                    placeholder="输入牌名"
                    class="w-full"
                  />
                </UFormField>

                <UFormField
                  label="花色"
                  required
                >
                  <USelect
                    v-model="selectedCard.suit"
                    :items="suitOptions"
                    placeholder="选择花色"
                    class="w-full"
                  />
                </UFormField>
              </div>
            </UCard>

            <!-- 元素列表 -->
            <UCard>
              <template #header>
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-semibold">
                    牌面元素
                  </h3>
                  <UButton
                    icon="i-lucide-plus"
                    size="sm"
                    @click="addElement"
                  >
                    添加元素
                  </UButton>
                </div>
              </template>

              <div
                v-if="selectedCard.elements.length === 0"
                class="text-center py-8 text-gray-500"
              >
                暂无元素，点击上方按钮添加
              </div>

              <UAccordion
                v-else
                :items="selectedCard.elements.map((element, index) => ({
                  label: element.label || `元素 ${index + 1}`,
                  slot: `element-${index}`,
                  defaultOpen: false
                }))"
              >
                <template
                  v-for="(element, elementIndex) in selectedCard.elements"
                  :key="elementIndex"
                  #[`element-${elementIndex}`]
                >
                  <div class="space-y-4 p-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <UFormField label="元素名称">
                        <UInput
                          v-model="element.label"
                          placeholder="输入元素名称"
                        />
                      </UFormField>

                      <div class="grid grid-cols-3 gap-2">
                        <UFormField label="X 坐标">
                          <UInputNumber v-model="element.x" />
                        </UFormField>
                        <UFormField label="Y 坐标">
                          <UInputNumber v-model="element.y" />
                        </UFormField>
                        <UFormField label="半径">
                          <UInputNumber v-model="element.r" />
                        </UFormField>
                      </div>
                    </div>

                    <!-- 元素详情 -->
                    <div class="border-t border-default pt-4">
                      <div class="flex items-center justify-between mb-3">
                        <h4 class="font-medium">
                          详情描述
                        </h4>
                        <UButton
                          icon="i-lucide-plus"
                          size="sm"
                          variant="soft"
                          @click="addDetail(elementIndex)"
                        >
                          添加详情
                        </UButton>
                      </div>

                      <div class="space-y-3">
                        <div
                          v-for="(detail, detailIndex) in element.details"
                          :key="detailIndex"
                          class="flex flex-col gap-2"
                        >
                          <div class="flex gap-2">
                            <USelect
                              v-model="detail.type"
                              :items="detailTypeOptions"
                              class="w-full"
                            />
                            <UButton
                              icon="i-lucide-trash-2"
                              color="error"
                              variant="ghost"
                              size="sm"
                              @click="removeDetail(elementIndex, detailIndex)"
                            />
                          </div>
                          <UTextarea
                            v-model="detail.content"
                            :rows="2"
                            placeholder="输入详情内容"
                            class="flex-1"
                          />
                        </div>
                      </div>
                    </div>

                    <div class="flex justify-end pt-2">
                      <UButton
                        icon="i-lucide-trash-2"
                        color="error"
                        variant="soft"
                        size="sm"
                        @click="removeElement(elementIndex)"
                      >
                        删除元素
                      </UButton>
                    </div>
                  </div>
                </template>
              </UAccordion>
            </UCard>

            <!-- 含义详解 -->
            <CardMeanings v-model="selectedCard.meanings" />
          </div>

          <div
            v-else
            class="flex items-center justify-center h-64"
          >
            <UEmpty
              description="请从左侧选择一张牌"
              icon="i-lucide-layers"
            />
          </div>

          <!-- 导入模态框 -->
          <UModal
            v-model:open="isImportModal"
            title="导入数据"
          >
            <template #body>
              <UFormField label="JSON 数据">
                <UTextarea
                  v-model="importJson"
                  :rows="10"
                  placeholder="粘贴 JSON 数据..."
                  class="w-full"
                />
              </UFormField>
            </template>
            <template #footer>
              <div class="flex gap-2 justify-end w-full">
                <UButton
                  variant="outline"
                  @click="isImportModal = false"
                >
                  取消
                </UButton>
                <UButton
                  icon="i-lucide-upload"
                  @click="importData"
                >
                  导入
                </UButton>
              </div>
            </template>
          </UModal>
        </UPageBody>
      </UPage>
    </UContainer>
  </div>
</template>

<script setup lang="ts">
interface Detail {
  type: 'visual' | 'symbolism' | 'interpretation'
  content: string
}

interface Element {
  label: string
  x: number
  y: number
  r: number
  details: Detail[]
}

interface Scenario {
  type: 'relationship' | 'business' | 'wealth'
  content: string
}

interface Meaning {
  meaning: string
  keywords: string[]
  summary: string
  scenarios: Scenario[]
}

interface Card {
  suit: string
  label: string
  elements: Element[]
  meanings: {
    upright: Meaning
    reversed: Meaning
  }
}

const toast = useToast()

// State
const cards = ref<Card[]>([])
const selectedCardIndex = ref<number | null>(null)
const searchQuery = ref('')
const isSaving = ref(false)
const isImportModal = ref(false)
const importJson = ref('')

// Options
const suitOptions = [
  { label: '大牌', value: 'major' },
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
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error ignore
    selectedCard.value.elements[elementIndex].details.push({
      type: 'visual',
      content: ''
    })
  }
}

const removeDetail = (elementIndex: number, detailIndex: number) => {
  if (selectedCard.value) {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error ignore
    selectedCard.value.elements[elementIndex].details.splice(detailIndex, 1)
  }
}

const saveData = async () => {
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

// Init
onMounted(() => {
  initializeCards()
})
</script>
