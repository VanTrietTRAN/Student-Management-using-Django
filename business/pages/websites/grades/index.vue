<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý điểm số</h1>
                    <p class="text-gray-600">Nhập điểm, xem điểm, thống kê kết quả học tập của sinh viên</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Nhập điểm mới
                </el-button>
            </div>
        </div>

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên sinh viên..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedClass" placeholder="Chọn lớp" clearable>
                    <el-option label="Tất cả lớp" value="" />
                    <el-option label="CNTT21A" value="CNTT21A" />
                    <el-option label="CNTT21B" value="CNTT21B" />
                    <el-option label="CNTT22A" value="CNTT22A" />
                </el-select>
                <el-select v-model="selectedSubject" placeholder="Chọn môn học" clearable>
                    <el-option label="Tất cả môn" value="" />
                    <el-option label="Lập trình Cơ bản" value="CS101" />
                    <el-option label="Cấu trúc dữ liệu" value="CS102" />
                    <el-option label="Lập trình Web" value="CS201" />
                </el-select>
                <el-select v-model="selectedSemester" placeholder="Học kỳ" clearable>
                    <el-option label="Tất cả học kỳ" value="" />
                    <el-option label="Học kỳ 1" value="1" />
                    <el-option label="Học kỳ 2" value="2" />
                    <el-option label="Học kỳ 3" value="3" />
                </el-select>
                <el-button type="primary" :icon="Search" @click="handleSearch">
                    Tìm kiếm
                </el-button>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="flex items-center">
                    <div class="p-3 bg-blue-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng điểm đã nhập</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalGrades }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Điểm TB cao nhất</p>
                        <p class="text-2xl font-bold text-gray-900">{{ highestGPA }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="flex items-center">
                    <div class="p-3 bg-purple-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-purple-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Điểm TB thấp nhất</p>
                        <p class="text-2xl font-bold text-gray-900">{{ lowestGPA }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Điểm TB trung bình</p>
                        <p class="text-2xl font-bold text-gray-900">{{ averageGPA }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Grades Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách điểm số</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredGrades" stripe style="width: 100%">
                    <el-table-column prop="studentId" label="Mã SV" width="100" />
                    <el-table-column prop="studentName" label="Tên sinh viên" width="200" />
                    <el-table-column prop="className" label="Lớp" width="100" />
                    <el-table-column prop="subjectCode" label="Mã môn" width="100" />
                    <el-table-column prop="subjectName" label="Tên môn học" width="200" />
                    <el-table-column prop="semester" label="HK" width="80" />
                    <el-table-column prop="midtermScore" label="Điểm GK" width="100" />
                    <el-table-column prop="finalScore" label="Điểm CK" width="100" />
                    <el-table-column prop="averageScore" label="Điểm TB" width="100">
                        <template #default="scope">
                            <span :class="getScoreClass(scope.row.averageScore)">
                                {{ scope.row.averageScore }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="grade" label="Xếp loại" width="100">
                        <template #default="scope">
                            <el-tag :type="getGradeType(scope.row.grade)">
                                {{ scope.row.grade }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="150">
                        <template #default="scope">
                            <el-button size="small" @click="viewGrade(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editGrade(scope.row)">
                                Sửa
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="p-4 border-t border-gray-200">
                <el-pagination
                    v-model:current-page="currentPage"
                    v-model:page-size="pageSize"
                    :page-sizes="[10, 20, 50, 100]"
                    :total="totalGrades"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Grade Dialog -->
        <el-dialog v-model="showAddDialog" title="Nhập điểm mới" width="600px">
            <el-form :model="newGrade" label-width="120px">
                <el-form-item label="Sinh viên">
                    <el-select v-model="newGrade.studentId" placeholder="Chọn sinh viên" filterable>
                        <el-option 
                            v-for="student in students" 
                            :key="student.id" 
                            :label="`${student.studentId} - ${student.fullName}`" 
                            :value="student.studentId" 
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="Môn học">
                    <el-select v-model="newGrade.subjectCode" placeholder="Chọn môn học">
                        <el-option 
                            v-for="subject in subjects" 
                            :key="subject.id" 
                            :label="`${subject.subjectCode} - ${subject.subjectName}`" 
                            :value="subject.subjectCode" 
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="Học kỳ">
                    <el-input-number v-model="newGrade.semester" :min="1" :max="8" />
                </el-form-item>
                <el-form-item label="Điểm giữa kỳ">
                    <el-input-number v-model="newGrade.midtermScore" :min="0" :max="10" :step="0.1" />
                </el-form-item>
                <el-form-item label="Điểm cuối kỳ">
                    <el-input-number v-model="newGrade.finalScore" :min="0" :max="10" :step="0.1" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addGrade">Thêm</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconAppraisal from '@/assets/icons/appraisal.svg';

definePageMeta({
    layout: 'websites'
});

// Reactive data
const searchKeyword = ref('');
const selectedClass = ref('');
const selectedSubject = ref('');
const selectedSemester = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedGrade = ref(null);
const editingGrade = ref({});

const newGrade = ref({
    studentId: '',
    subjectCode: '',
    semester: 1,
    midtermScore: 0,
    finalScore: 0
});

// Mock data
const students = ref([
    { id: 1, studentId: 'SV001', fullName: 'Nguyễn Văn An' },
    { id: 2, studentId: 'SV002', fullName: 'Trần Thị Bình' },
    { id: 3, studentId: 'SV003', fullName: 'Lê Văn Cường' }
]);

const subjects = ref([
    { id: 1, subjectCode: 'CS101', subjectName: 'Lập trình Cơ bản' },
    { id: 2, subjectCode: 'CS102', subjectName: 'Cấu trúc dữ liệu' },
    { id: 3, subjectCode: 'CS201', subjectName: 'Lập trình Web' }
]);

const grades = ref([
    {
        id: 1,
        studentId: 'SV001',
        studentName: 'Nguyễn Văn An',
        className: 'CNTT21A',
        subjectCode: 'CS101',
        subjectName: 'Lập trình Cơ bản',
        semester: 1,
        midtermScore: 8.5,
        finalScore: 9.0,
        averageScore: 8.75,
        grade: 'A'
    },
    {
        id: 2,
        studentId: 'SV002',
        studentName: 'Trần Thị Bình',
        className: 'CNTT21B',
        subjectCode: 'CS102',
        subjectName: 'Cấu trúc dữ liệu',
        semester: 2,
        midtermScore: 7.0,
        finalScore: 8.5,
        averageScore: 7.75,
        grade: 'B+'
    },
    {
        id: 3,
        studentId: 'SV003',
        studentName: 'Lê Văn Cường',
        className: 'CNTT22A',
        subjectCode: 'CS201',
        subjectName: 'Lập trình Web',
        semester: 3,
        midtermScore: 9.5,
        finalScore: 9.0,
        averageScore: 9.25,
        grade: 'A+'
    }
]);

// Computed properties
const totalGrades = computed(() => grades.value.length);
const highestGPA = computed(() => {
    const scores = grades.value.map(g => g.averageScore);
    return scores.length > 0 ? Math.max(...scores).toFixed(2) : '0.00';
});
const lowestGPA = computed(() => {
    const scores = grades.value.map(g => g.averageScore);
    return scores.length > 0 ? Math.min(...scores).toFixed(2) : '0.00';
});
const averageGPA = computed(() => {
    const scores = grades.value.map(g => g.averageScore);
    return scores.length > 0 ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(2) : '0.00';
});

const filteredGrades = computed(() => {
    let filtered = grades.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(grade => 
            grade.studentName.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedClass.value) {
        filtered = filtered.filter(grade => grade.className === selectedClass.value);
    }
    
    if (selectedSubject.value) {
        filtered = filtered.filter(grade => grade.subjectCode === selectedSubject.value);
    }
    
    if (selectedSemester.value) {
        filtered = filtered.filter(grade => grade.semester.toString() === selectedSemester.value);
    }
    
    return filtered;
});

// Methods
const getScoreClass = (score: number) => {
    if (score >= 8.5) return 'text-green-600 font-bold';
    if (score >= 7.0) return 'text-blue-600 font-bold';
    if (score >= 5.5) return 'text-yellow-600 font-bold';
    return 'text-red-600 font-bold';
};

const getGradeType = (grade: string) => {
    switch (grade) {
        case 'A+':
        case 'A': return 'success';
        case 'B+':
        case 'B': return 'primary';
        case 'C+':
        case 'C': return 'warning';
        case 'D+':
        case 'D': return 'info';
        case 'F': return 'danger';
        default: return 'info';
    }
};

const handleSearch = () => {
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewGrade = (grade: any) => {
    selectedGrade.value = grade;
    showViewDialog.value = true;
};

const editGrade = (grade: any) => {
    editingGrade.value = { ...grade };
    showEditDialog.value = true;
};

const editGradeFromView = () => {
    showViewDialog.value = false;
    editingGrade.value = { ...selectedGrade.value };
    showEditDialog.value = true;
};

const updateGrade = () => {
    const index = grades.value.findIndex(g => g.id === editingGrade.value.id);
    if (index > -1) {
        grades.value[index] = { ...editingGrade.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật điểm: ${editingGrade.value.studentName} - ${editingGrade.value.subjectName}`);
    }
};

const addGrade = () => {
    if (newGrade.value.studentId && newGrade.value.subjectCode) {
        const student = students.value.find(s => s.studentId === newGrade.value.studentId);
        const subject = subjects.value.find(s => s.subjectCode === newGrade.value.subjectCode);
        
        if (student && subject) {
            const averageScore = (newGrade.value.midtermScore + newGrade.value.finalScore) / 2;
            const grade = getGradeFromScore(averageScore);
            
            grades.value.push({
                id: grades.value.length + 1,
                studentId: newGrade.value.studentId,
                studentName: student.fullName,
                className: 'CNTT21A', // Default class
                subjectCode: newGrade.value.subjectCode,
                subjectName: subject.subjectName,
                semester: newGrade.value.semester,
                midtermScore: newGrade.value.midtermScore,
                finalScore: newGrade.value.finalScore,
                averageScore: averageScore,
                grade: grade
            });
            
            showAddDialog.value = false;
            newGrade.value = {
                studentId: '',
                subjectCode: '',
                semester: 1,
                midtermScore: 0,
                finalScore: 0
            };
            ElMessage.success('Thêm điểm thành công');
        }
    } else {
        ElMessage.error('Vui lòng điền đầy đủ thông tin');
    }
};

const getGradeFromScore = (score: number) => {
    if (score >= 9.5) return 'A+';
    if (score >= 8.5) return 'A';
    if (score >= 8.0) return 'B+';
    if (score >= 7.0) return 'B';
    if (score >= 6.5) return 'C+';
    if (score >= 5.5) return 'C';
    if (score >= 5.0) return 'D+';
    if (score >= 4.0) return 'D';
    return 'F';
};
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
