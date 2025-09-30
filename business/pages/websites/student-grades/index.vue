<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Điểm số của tôi</h1>
            <p class="text-gray-600">Xem điểm số chi tiết và tổng hợp theo từng học kỳ</p>
        </div>

        <!-- Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <el-select v-model="selectedSemester" placeholder="Chọn học kỳ" clearable>
                    <el-option label="Tất cả học kỳ" value="" />
                    <el-option label="Học kỳ 1" value="1" />
                    <el-option label="Học kỳ 2" value="2" />
                    <el-option label="Học kỳ 3" value="3" />
                </el-select>
                <el-select v-model="selectedYear" placeholder="Chọn năm học" clearable>
                    <el-option label="Tất cả năm" value="" />
                    <el-option label="2021-2022" value="2021-2022" />
                    <el-option label="2022-2023" value="2022-2023" />
                    <el-option label="2023-2024" value="2023-2024" />
                </el-select>
                <el-button type="primary" :icon="Search" @click="handleFilter">
                    Lọc kết quả
                </el-button>
            </div>
        </div>

        <!-- GPA Summary -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">GPA hiện tại</p>
                        <p class="text-2xl font-bold text-gray-900">{{ currentGPA }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Môn đã hoàn thành</p>
                        <p class="text-2xl font-bold text-gray-900">{{ completedSubjects }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Môn đang học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ currentSubjects }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng tín chỉ</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalCredits }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Grades Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Chi tiết điểm số</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredGrades" stripe style="width: 100%">
                    <el-table-column prop="subjectCode" label="Mã môn" width="120" />
                    <el-table-column prop="subjectName" label="Tên môn học" width="200" />
                    <el-table-column prop="credits" label="Tín chỉ" width="100" />
                    <el-table-column prop="semester" label="Học kỳ" width="100" />
                    <el-table-column prop="midtermScore" label="Giữa kỳ" width="100" />
                    <el-table-column prop="finalScore" label="Cuối kỳ" width="100" />
                    <el-table-column prop="gpa" label="Điểm TB" width="100">
                        <template #default="scope">
                            <span :class="getGPAClass(scope.row.gpa)" class="font-bold">
                                {{ scope.row.gpa }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="120">
                        <template #default="scope">
                            <el-button size="small" @click="viewGradeDetail(scope.row)">
                                Xem chi tiết
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </div>

        <!-- Grade Detail Dialog -->
        <el-dialog v-model="showDetailDialog" title="Chi tiết điểm số" width="600px">
            <div v-if="selectedGrade" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Môn học</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedGrade.subjectName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Mã môn</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedGrade.subjectCode }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Học kỳ</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedGrade.semester }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Tín chỉ</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedGrade.credits }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Điểm giữa kỳ</label>
                        <p class="mt-1 text-sm text-gray-900 font-bold">{{ selectedGrade.midtermScore }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Điểm cuối kỳ</label>
                        <p class="mt-1 text-sm text-gray-900 font-bold">{{ selectedGrade.finalScore }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Điểm TB</label>
                        <p class="mt-1 text-sm text-gray-900 font-bold text-lg" :class="getGPAClass(selectedGrade.gpa)">
                            {{ selectedGrade.gpa }}
                        </p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="getStatusType(selectedGrade.status)">
                            {{ selectedGrade.status }}
                        </el-tag>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showDetailDialog = false">Đóng</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { Search } from '@element-plus/icons-vue';
import IconAppraisal from '@/assets/icons/appraisal.svg';

definePageMeta({
    layout: 'student'
});

// Reactive data
const selectedSemester = ref('');
const selectedYear = ref('');
const showDetailDialog = ref(false);
const selectedGrade = ref(null);

// Mock data
const grades = ref([
    {
        id: 1,
        subjectCode: 'CS101',
        subjectName: 'Lập trình cơ bản',
        credits: 3,
        semester: '1',
        year: '2021-2022',
        midtermScore: 8.5,
        finalScore: 9.0,
        gpa: 8.8,
        status: 'Hoàn thành'
    },
    {
        id: 2,
        subjectCode: 'CS102',
        subjectName: 'Cấu trúc dữ liệu',
        credits: 4,
        semester: '2',
        year: '2021-2022',
        midtermScore: 7.5,
        finalScore: 8.0,
        gpa: 7.8,
        status: 'Hoàn thành'
    },
    {
        id: 3,
        subjectCode: 'SE201',
        subjectName: 'Phát triển phần mềm',
        credits: 3,
        semester: '1',
        year: '2022-2023',
        midtermScore: 9.0,
        finalScore: 9.5,
        gpa: 9.3,
        status: 'Hoàn thành'
    },
    {
        id: 4,
        subjectCode: 'IT301',
        subjectName: 'An toàn thông tin',
        credits: 3,
        semester: '2',
        year: '2022-2023',
        midtermScore: 8.0,
        finalScore: 8.5,
        gpa: 8.4,
        status: 'Hoàn thành'
    }
]);

// Computed properties
const currentGPA = computed(() => {
    const total = grades.value.reduce((sum, g) => sum + g.gpa, 0);
    return (total / grades.value.length).toFixed(1);
});

const completedSubjects = computed(() => grades.value.filter(g => g.status === 'Hoàn thành').length);
const currentSubjects = computed(() => grades.value.filter(g => g.status === 'Đang học').length);
const totalCredits = computed(() => grades.value.reduce((sum, g) => sum + g.credits, 0));

const filteredGrades = computed(() => {
    let filtered = grades.value;
    
    if (selectedSemester.value) {
        filtered = filtered.filter(grade => grade.semester === selectedSemester.value);
    }
    
    if (selectedYear.value) {
        filtered = filtered.filter(grade => grade.year === selectedYear.value);
    }
    
    return filtered;
});

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Hoàn thành': return 'success';
        case 'Đang học': return 'warning';
        case 'Thi lại': return 'danger';
        default: return 'info';
    }
};

const getGPAClass = (gpa: number) => {
    if (gpa >= 8.0) return 'text-green-600';
    if (gpa >= 6.5) return 'text-blue-600';
    if (gpa >= 5.0) return 'text-yellow-600';
    return 'text-red-600';
};

const handleFilter = () => {
    ElMessage.success('Lọc kết quả hoàn tất');
};

const viewGradeDetail = (grade: any) => {
    selectedGrade.value = grade;
    showDetailDialog.value = true;
};
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
