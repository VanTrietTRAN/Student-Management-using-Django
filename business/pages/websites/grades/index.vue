<template>
    <div class="min-h-screen bg-gray-50 pt-20 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý điểm số</h1>
                    <p class="text-gray-600">Nhập điểm, sửa điểm, xem điểm và thống kê kết quả học tập</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Nhập điểm mới
                </el-button>
            </div>
        </div>

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên sinh viên..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedSubject" placeholder="Chọn môn học" clearable>
                    <el-option label="Tất cả môn" value="" />
                    <el-option label="Lập trình cơ bản" value="CS101" />
                    <el-option label="Cấu trúc dữ liệu" value="CS102" />
                    <el-option label="Phát triển phần mềm" value="SE201" />
                </el-select>
                <el-select v-model="selectedSemester" placeholder="Chọn học kỳ" clearable>
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
                        <p class="text-sm font-medium text-gray-600">Tổng điểm</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalGrades }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Điểm TB hệ thống</p>
                        <p class="text-2xl font-bold text-gray-900">{{ systemGPA }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Sinh viên giỏi</p>
                        <p class="text-2xl font-bold text-gray-900">{{ excellentStudents }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                <div class="flex items-center">
                    <div class="p-3 bg-red-100 rounded-full">
                        <IconAppraisal class="w-8 h-8 text-red-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Sinh viên yếu</p>
                        <p class="text-2xl font-bold text-gray-900">{{ weakStudents }}</p>
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
                    <el-table-column prop="studentName" label="Sinh viên" width="180" />
                    <el-table-column prop="subjectName" label="Môn học" width="200" />
                    <el-table-column prop="semester" label="Học kỳ" width="100" />
                    <el-table-column prop="midtermScore" label="Điểm giữa kỳ" width="120" />
                    <el-table-column prop="finalScore" label="Điểm cuối kỳ" width="120" />
                    <el-table-column prop="gpa" label="Điểm TB" width="100">
                        <template #default="scope">
                            <span :class="getGPAClass(scope.row.gpa)">{{ scope.row.gpa }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewGrade(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editGrade(scope.row)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click="deleteGrade(scope.row)">
                                Xóa
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
                    <el-select v-model="newGrade.studentName" placeholder="Chọn sinh viên">
                        <el-option label="Nguyễn Văn An" value="Nguyễn Văn An" />
                        <el-option label="Trần Thị Bình" value="Trần Thị Bình" />
                        <el-option label="Lê Văn Cường" value="Lê Văn Cường" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Môn học">
                    <el-select v-model="newGrade.subjectName" placeholder="Chọn môn học">
                        <el-option label="Lập trình cơ bản" value="Lập trình cơ bản" />
                        <el-option label="Cấu trúc dữ liệu" value="Cấu trúc dữ liệu" />
                        <el-option label="Phát triển phần mềm" value="Phát triển phần mềm" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Học kỳ">
                    <el-select v-model="newGrade.semester" placeholder="Chọn học kỳ">
                        <el-option label="Học kỳ 1" value="1" />
                        <el-option label="Học kỳ 2" value="2" />
                        <el-option label="Học kỳ 3" value="3" />
                    </el-select>
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

        <!-- View Grade Dialog -->
        <el-dialog v-model="showViewDialog" title="Chi tiết điểm số" width="800px">
            <div v-if="selectedGrade" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Sinh viên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedGrade.studentName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Môn học</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedGrade.subjectName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Học kỳ</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedGrade.semester }}</p>
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
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editGradeFromView">Chỉnh sửa</el-button>
            </template>
        </el-dialog>

        <!-- Edit Grade Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa điểm số" width="600px">
            <el-form :model="editingGrade" label-width="120px">
                <el-form-item label="Sinh viên">
                    <el-input v-model="editingGrade.studentName" disabled />
                </el-form-item>
                <el-form-item label="Môn học">
                    <el-input v-model="editingGrade.subjectName" disabled />
                </el-form-item>
                <el-form-item label="Học kỳ">
                    <el-input v-model="editingGrade.semester" disabled />
                </el-form-item>
                <el-form-item label="Điểm giữa kỳ">
                    <el-input-number v-model="editingGrade.midtermScore" :min="0" :max="10" :step="0.1" />
                </el-form-item>
                <el-form-item label="Điểm cuối kỳ">
                    <el-input-number v-model="editingGrade.finalScore" :min="0" :max="10" :step="0.1" />
                </el-form-item>
                <el-form-item label="Trạng thái">
                    <el-select v-model="editingGrade.status" placeholder="Chọn trạng thái">
                        <el-option label="Hoàn thành" value="Hoàn thành" />
                        <el-option label="Chưa hoàn thành" value="Chưa hoàn thành" />
                        <el-option label="Thi lại" value="Thi lại" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateGrade">Cập nhật</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconAppraisal from '@/assets/icons/appraisal.svg';
import IconUsers from '@/assets/icons/users.svg';

definePageMeta({
    layout: 'websites'
});

// Reactive data
const searchKeyword = ref('');
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
    studentName: '',
    subjectName: '',
    semester: '',
    midtermScore: 0,
    finalScore: 0
});

// Mock data
const grades = ref([
    {
        id: 1,
        studentName: 'Nguyễn Văn An',
        subjectName: 'Lập trình cơ bản',
        semester: '1',
        midtermScore: 8.5,
        finalScore: 9.0,
        gpa: 8.8,
        status: 'Hoàn thành'
    },
    {
        id: 2,
        studentName: 'Trần Thị Bình',
        subjectName: 'Cấu trúc dữ liệu',
        semester: '2',
        midtermScore: 7.5,
        finalScore: 8.0,
        gpa: 7.8,
        status: 'Hoàn thành'
    },
    {
        id: 3,
        studentName: 'Lê Văn Cường',
        subjectName: 'Phát triển phần mềm',
        semester: '3',
        midtermScore: 9.0,
        finalScore: 9.5,
        gpa: 9.3,
        status: 'Hoàn thành'
    }
]);

// Computed properties
const totalGrades = computed(() => grades.value.length);
const systemGPA = computed(() => {
    const total = grades.value.reduce((sum, g) => sum + g.gpa, 0);
    return (total / grades.value.length).toFixed(1);
});
const excellentStudents = computed(() => grades.value.filter(g => g.gpa >= 8.0).length);
const weakStudents = computed(() => grades.value.filter(g => g.gpa < 5.0).length);

const filteredGrades = computed(() => {
    let filtered = grades.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(grade => 
            grade.studentName.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedSubject.value) {
        filtered = filtered.filter(grade => grade.subjectName === selectedSubject.value);
    }
    
    if (selectedSemester.value) {
        filtered = filtered.filter(grade => grade.semester === selectedSemester.value);
    }
    
    return filtered;
});

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Hoàn thành': return 'success';
        case 'Chưa hoàn thành': return 'warning';
        case 'Thi lại': return 'danger';
        default: return 'info';
    }
};

const getGPAClass = (gpa: number) => {
    if (gpa >= 8.0) return 'text-green-600 font-bold';
    if (gpa >= 6.5) return 'text-blue-600 font-bold';
    if (gpa >= 5.0) return 'text-yellow-600 font-bold';
    return 'text-red-600 font-bold';
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
        // Auto-calculate GPA
        const midterm = editingGrade.value.midtermScore || 0;
        const final = editingGrade.value.finalScore || 0;
        editingGrade.value.gpa = ((midterm * 0.3) + (final * 0.7)).toFixed(1);
        
        grades.value[index] = { ...editingGrade.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật điểm: ${editingGrade.value.studentName}`);
    }
};

const deleteGrade = (grade: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa điểm của "${grade.studentName}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        const index = grades.value.findIndex(g => g.id === grade.id);
        if (index > -1) {
            grades.value.splice(index, 1);
            ElMessage.success(`Đã xóa điểm: ${grade.studentName}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa điểm');
    });
};

const addGrade = () => {
    if (newGrade.value.studentName && newGrade.value.subjectName) {
        const midterm = newGrade.value.midtermScore || 0;
        const final = newGrade.value.finalScore || 0;
        const gpa = ((midterm * 0.3) + (final * 0.7)).toFixed(1);
        
        grades.value.push({
            id: grades.value.length + 1,
            ...newGrade.value,
            gpa: parseFloat(gpa),
            status: 'Hoàn thành'
        });
        showAddDialog.value = false;
        newGrade.value = {
            studentName: '',
            subjectName: '',
            semester: '',
            midtermScore: 0,
            finalScore: 0
        };
        ElMessage.success('Thêm điểm thành công');
    } else {
        ElMessage.error('Vui lòng điền đầy đủ thông tin');
    }
};
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>