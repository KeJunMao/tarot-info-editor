<template>
  <div>
    <UContainer>
      <UPage>
        <UPageHeader :headline="selectedCard?.suit">
          <template #title>
            <div class="flex items-center gap-3">
              <img
                v-if="selectedCard"
                :src="`${selectedCard.image.replace('assets/common', '')}`"
                class="h-[2em]"
              >
              {{ selectedCard ? selectedCard.label : '塔罗牌信息编辑器' }}
            </div>
          </template>
          <template #links>
            <UButton
              icon="i-lucide-save"
              :loading="isSaving"
              color="error"
              @click="saveData"
            >
              保存所有数据
            </UButton>
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
              @click="saveCurrentCard"
            >
              保存此牌
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
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <h3 class="text-lg font-semibold">
                      基本信息
                    </h3>
                  </div>
                </div>
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
                  <div class="flex gap-2">
                    <UButton
                      icon="i-lucide-plus"
                      size="sm"
                      variant="soft"
                      @click="isHotspotEditorOpen = true"
                    >
                      编辑热区
                    </UButton>
                    <UButton
                      icon="i-lucide-plus"
                      size="sm"
                      @click="addElement"
                    >
                      添加元素
                    </UButton>
                  </div>
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

          <!-- 热区编辑器模态框 -->
          <UModal
            v-model:open="isHotspotEditorOpen"
            title="编辑热区"
          >
            <template #body>
              <HotspotEditor
                v-if="selectedCard"
                :image-url="selectedCard.image ? selectedCard.image.replace('assets/common', '') : ''"
                :elements="selectedCard.elements"
              />
            </template>
          </UModal>
        </UPageBody>
      </UPage>
    </UContainer>
  </div>
</template>

<script setup lang="ts">
// 使用全局共享的 composable
const {
  // State
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
  initializeCards,
  addElement,
  removeElement,
  addDetail,
  removeDetail,
  saveData,
  saveCurrentCard,
  exportData,
  importData
} = useTarotCards()

// Init
onMounted(() => {
  initializeCards()
})
</script>
