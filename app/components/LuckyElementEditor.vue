<script setup lang="ts">
import type { LuckyElement } from '#shared/types/tarot'

const model = defineModel<LuckyElement>({ required: true })

const colorMap: Record<string, string> = {
  pale_yellow: '淡黄',
  neon_yellow: '霓虹黄',
  yellow: '黄色',
  orange: '橙色',
  blue: '蓝色',
  silver_white: '银白',
  green: '绿色',
  emerald: '祖母绿',
  red: '红色',
  crimson: '绯红',
  red_orange: '红橙',
  deep_purple: '深紫',
  light_purple: '浅紫',
  amber_color: '琥珀色',
  silver_gray: '银灰',
  gold: '金色',
  gray: '灰色',
  purple: '紫色',
  royal_blue: '宝蓝',
  indigo: '靛蓝',
  navy_blue: '深蓝',
  sea_green: '海绿',
  teal: '蓝绿',
  black: '黑色',
  iridescent: '虹色',
  indigo_blue: '靛青',
  scarlet: '猩红',
  electric_blue: '电光蓝',
  silver_red: '银红',
  golden_yellow: '金黄',
  gray_white: '灰白',
  bright_red: '亮红',
  white: '白色',
  rust_red: '铁锈红',
  tender_green: '嫩绿',
  dark_gray: '深灰',
  orange_red: '橙红',
  bright_yellow: '亮黄',
  silver_purple: '银紫',
  tan: '黄褐',
  gold_red: '金红',
  pink: '粉红',
  orange_yellow: '橙黄',
  dark_red: '暗红',
  copper_green: '铜绿',
  purple_blue: '紫蓝',
  dark_brown: '深褐',
  brown: '褐色',
  silver_blue: '银蓝',
  orange_gold: '橙金',
  light_blue: '淡蓝',
  bright_blue: '亮蓝',
  violet: '紫罗兰',
  iron_red: '铁红',
  olive_green: '橄榄绿',
  olive: '橄榄'
}

const crystalMap: Record<string, string> = {
  clear_quartz: '白水晶',
  laser_quartz: '激光柱',
  citrine: '黄水晶',
  amethyst: '紫水晶',
  deep_amethyst: '深紫晶',
  lavender: '薰衣草紫晶',
  rose_quartz: '粉晶',
  morganite: '摩根石',
  strawberry: '草莓晶',
  rhodochrosite: '红纹石',
  carnelian: '红玛瑙',
  garnet: '石榴石',
  obsidian: '黑曜石',
  smoky_quartz: '烟晶',
  hematite: '赤铁矿',
  tigers_eye: '虎眼石',
  golden_tiger: '金虎眼',
  moonstone: '月光石',
  grey_moon: '灰月光',
  labradorite: '拉长石',
  fluorite: '萤石',
  sunstone: '日光石',
  amber: '琥珀',
  rutilated: '金发晶'
}

const colorOptions = Object.entries(colorMap).map(([value, label]) => ({ label, value }))
const crystalOptions = Object.entries(crystalMap).map(([value, label]) => ({ label, value }))

const newColor = ref('')
const newCrystal = ref('')
const newNumber = ref<number | null>(null)

const availableColors = computed(() =>
  colorOptions.filter(opt => !model.value.colors.includes(opt.value))
)

const availableCrystals = computed(() =>
  crystalOptions.filter(opt => !model.value.crystals.includes(opt.value))
)

const addColor = () => {
  if (newColor.value && !model.value.colors.includes(newColor.value)) {
    model.value.colors.push(newColor.value)
    newColor.value = ''
  }
}

const addCrystal = () => {
  if (newCrystal.value && !model.value.crystals.includes(newCrystal.value)) {
    model.value.crystals.push(newCrystal.value)
    newCrystal.value = ''
  }
}

const addNumber = () => {
  if (newNumber.value !== null && !model.value.numbers.includes(newNumber.value)) {
    model.value.numbers.push(newNumber.value)
    newNumber.value = null
  }
}

const removeColor = (index: number) => {
  model.value.colors.splice(index, 1)
}

const removeCrystal = (index: number) => {
  model.value.crystals.splice(index, 1)
}

const removeNumber = (index: number) => {
  model.value.numbers.splice(index, 1)
}
</script>

<template>
  <UCard>
    <template #header>
      <h3 class="text-lg font-semibold">
        幸运元素
      </h3>
    </template>

    <div class="space-y-6">
      <!-- 幸运颜色 -->
      <UFormField label="幸运颜色">
        <div
          v-if="model.colors.length"
          class="flex flex-wrap gap-2 mb-2"
        >
          <span
            v-for="(color, i) in model.colors"
            :key="i"
            class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-primary/10 text-primary text-sm"
          >
            {{ colorMap[color] || color }}
            <UIcon
              name="i-lucide-x"
              class="size-3 cursor-pointer opacity-60 hover:opacity-100"
              @click="removeColor(i)"
            />
          </span>
        </div>
        <div class="flex gap-2">
          <USelect
            v-model="newColor"
            :items="availableColors"
            placeholder="选择颜色"
            class="flex-1"
          />
          <UButton
            icon="i-lucide-plus"
            size="sm"
            variant="soft"
            :disabled="!newColor"
            @click="addColor"
          />
        </div>
      </UFormField>

      <!-- 幸运水晶 -->
      <UFormField label="幸运水晶">
        <div
          v-if="model.crystals.length"
          class="flex flex-wrap gap-2 mb-2"
        >
          <span
            v-for="(crystal, i) in model.crystals"
            :key="i"
            class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-primary/10 text-primary text-sm"
          >
            {{ crystalMap[crystal] || crystal }}
            <UIcon
              name="i-lucide-x"
              class="size-3 cursor-pointer opacity-60 hover:opacity-100"
              @click="removeCrystal(i)"
            />
          </span>
        </div>
        <div class="flex gap-2">
          <USelect
            v-model="newCrystal"
            :items="availableCrystals"
            placeholder="选择水晶"
            class="flex-1"
          />
          <UButton
            icon="i-lucide-plus"
            size="sm"
            variant="soft"
            :disabled="!newCrystal"
            @click="addCrystal"
          />
        </div>
      </UFormField>

      <!-- 幸运数字 -->
      <UFormField label="幸运数字">
        <div
          v-if="model.numbers.length"
          class="flex flex-wrap gap-2 mb-2"
        >
          <span
            v-for="(num, i) in model.numbers"
            :key="i"
            class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-primary/10 text-primary text-sm"
          >
            {{ num }}
            <UIcon
              name="i-lucide-x"
              class="size-3 cursor-pointer opacity-60 hover:opacity-100"
              @click="removeNumber(i)"
            />
          </span>
        </div>
        <div class="flex gap-2">
          <UInputNumber
            v-model="newNumber"
            placeholder="输入数字"
            class="flex-1"
          />
          <UButton
            icon="i-lucide-plus"
            size="sm"
            variant="soft"
            :disabled="newNumber === null"
            @click="addNumber"
          />
        </div>
      </UFormField>
    </div>
  </UCard>
</template>
