<template>
    <div class="min-h-screen bg-gray-50 pt-32 px-4 md:px-6 pb-6">
        <!-- Header Section -->
        <div class="mb-8">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Quản lý sinh viên</h1>
                    <p class="text-gray-600">Quản lý hồ sơ sinh viên, thông tin cá nhân và quá trình học tập</p>
                </div>
                <el-button type="primary" :icon="Plus" @click="showAddDialog = true">
                    Thêm sinh viên mới
                </el-button>
            </div>
        </div>

        <!-- Search and Filter Section -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <el-input
                    v-model="searchKeyword"
                    placeholder="Tìm kiếm theo tên, mã sinh viên..."
                    :prefix-icon="Search"
                    clearable
                />
                <el-select v-model="selectedClass" placeholder="Chọn lớp" clearable>
                    <el-option label="Tất cả lớp" value="" />
                    <el-option label="CNTT21A" value="CNTT21A" />
                    <el-option label="CNTT21B" value="CNTT21B" />
                    <el-option label="CNTT22A" value="CNTT22A" />
                </el-select>
                <el-select v-model="selectedMajor" placeholder="Chọn ngành" clearable>
                    <el-option label="Tất cả ngành" value="" />
                    <el-option label="Công nghệ thông tin" value="CNTT" />
                    <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                    <el-option label="An toàn thông tin" value="ATTT" />
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
                        <IconUsers class="w-8 h-8 text-blue-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Tổng sinh viên</p>
                        <p class="text-2xl font-bold text-gray-900">{{ totalStudents }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                <div class="flex items-center">
                    <div class="p-3 bg-green-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-green-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Sinh viên đang học</p>
                        <p class="text-2xl font-bold text-gray-900">{{ activeStudents }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="flex items-center">
                    <div class="p-3 bg-orange-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-orange-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Sinh viên tốt nghiệp</p>
                        <p class="text-2xl font-bold text-gray-900">{{ graduatedStudents }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                <div class="flex items-center">
                    <div class="p-3 bg-red-100 rounded-full">
                        <IconUsers class="w-8 h-8 text-red-600" />
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">Sinh viên tạm nghỉ</p>
                        <p class="text-2xl font-bold text-gray-900">{{ suspendedStudents }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Students Table -->
        <div class="bg-white rounded-lg shadow-md">
            <div class="p-6 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Danh sách sinh viên</h3>
            </div>
            <div class="overflow-x-auto">
                <el-table :data="filteredStudents" stripe style="width: 100%">
                    <el-table-column prop="studentId" label="Mã sinh viên" width="120" />
                    <el-table-column prop="fullName" label="Họ và tên" width="200" />
                    <el-table-column prop="email" label="Email" width="200" />
                    <el-table-column prop="phone" label="Số điện thoại" width="130" />
                    <el-table-column prop="class" label="Lớp" width="100" />
                    <el-table-column prop="major" label="Ngành" width="150" />
                    <el-table-column prop="status" label="Trạng thái" width="120">
                        <template #default="scope">
                            <el-tag :type="getStatusType(scope.row.status)">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="gpa" label="Điểm TB" width="100" />
                    <el-table-column label="Thao tác" width="200">
                        <template #default="scope">
                            <el-button size="small" @click="viewStudent(scope.row)">
                                Xem
                            </el-button>
                            <el-button size="small" type="primary" @click="editStudent(scope.row)">
                                Sửa
                            </el-button>
                            <el-button size="small" type="danger" @click="deleteStudent(scope.row)">
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
                    :total="totalStudents"
                    layout="total, sizes, prev, pager, next, jumper"
                />
            </div>
        </div>

        <!-- Add Student Dialog -->
        <el-dialog v-model="showAddDialog" title="Thêm sinh viên mới" width="600px">
            <el-form :model="newStudent" label-width="120px">
                <el-form-item label="Mã sinh viên">
                    <el-input v-model="newStudent.studentId" />
                </el-form-item>
                <el-form-item label="Họ và tên">
                    <el-input v-model="newStudent.fullName" />
                </el-form-item>
                <el-form-item label="Email">
                    <el-input v-model="newStudent.email" type="email" />
                </el-form-item>
                <el-form-item label="Số điện thoại">
                    <el-input v-model="newStudent.phone" />
                </el-form-item>
                <el-form-item label="Lớp">
                    <el-select v-model="newStudent.class" placeholder="Chọn lớp">
                        <el-option label="CNTT21A" value="CNTT21A" />
                        <el-option label="CNTT21B" value="CNTT21B" />
                        <el-option label="CNTT22A" value="CNTT22A" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Ngành">
                    <el-select v-model="newStudent.major" placeholder="Chọn ngành">
                        <el-option label="Công nghệ thông tin" value="CNTT" />
                        <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                        <el-option label="An toàn thông tin" value="ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Ảnh đại diện">
                    <input type="file" accept="image/*" @change="onAddImageChange" />
                    <div v-if="newStudent.profile_picture_preview" class="mt-2">
                        <img :src="newStudent.profile_picture_preview" alt="Preview" class="w-24 h-24 object-cover rounded-full border" />
                    </div>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showAddDialog = false">Hủy</el-button>
                <el-button type="primary" @click="addStudent">Thêm</el-button>
            </template>
        </el-dialog>

        <!-- View Student Dialog -->
        <el-dialog v-model="showViewDialog" title="Thông tin sinh viên" width="800px">
            <div v-if="selectedStudent" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div class="col-span-2 flex flex-col items-center">
                        <label class="block text-sm font-medium text-gray-700">Ảnh thẻ</label>
                        <img v-if="selectedStudent.profile_picture" :src="getProfilePictureUrl(selectedStudent.profile_picture)" alt="Ảnh đại diện" class="w-32 h-32 object-cover rounded-full border mb-2" />
                        <span v-else class="text-gray-400">Chưa có ảnh</span>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Mã sinh viên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedStudent.studentId }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Họ và tên</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedStudent.fullName }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Email</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedStudent.email }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Số điện thoại</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedStudent.phone }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Lớp</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedStudent.class }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Ngành</label>
                        <p class="mt-1 text-sm text-gray-900">{{ selectedStudent.major }}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Trạng thái</label>
                        <el-tag :type="getStatusType(selectedStudent.status)">
                            {{ selectedStudent.status }}
                        </el-tag>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Điểm TB</label>
                        <p class="mt-1 text-sm text-gray-900 font-bold">{{ selectedStudent.gpa }}</p>
                    </div>
                </div>
            </div>
            <template #footer>
                <el-button @click="showViewDialog = false">Đóng</el-button>
                <el-button type="primary" @click="editStudentFromView">Chỉnh sửa</el-button>
            </template>
        </el-dialog>

        <!-- Edit Student Dialog -->
        <el-dialog v-model="showEditDialog" title="Chỉnh sửa sinh viên" width="600px">
            <el-form :model="editingStudent" label-width="120px">
                <el-form-item label="Mã sinh viên">
                    <el-input v-model="editingStudent.studentId" disabled />
                </el-form-item>
                <el-form-item label="Họ và tên">
                    <el-input v-model="editingStudent.fullName" />
                </el-form-item>
                <el-form-item label="Email">
                    <el-input v-model="editingStudent.email" type="email" />
                </el-form-item>
                <el-form-item label="Số điện thoại">
                    <el-input v-model="editingStudent.phone" />
                </el-form-item>
                <el-form-item label="Lớp">
                    <el-select v-model="editingStudent.class" placeholder="Chọn lớp">
                        <el-option label="CNTT21A" value="CNTT21A" />
                        <el-option label="CNTT21B" value="CNTT21B" />
                        <el-option label="CNTT22A" value="CNTT22A" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Ngành">
                    <el-select v-model="editingStudent.major" placeholder="Chọn ngành">
                        <el-option label="Công nghệ thông tin" value="CNTT" />
                        <el-option label="Kỹ thuật phần mềm" value="KTPM" />
                        <el-option label="An toàn thông tin" value="ATTT" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Trạng thái">
                    <el-select v-model="editingStudent.status" placeholder="Chọn trạng thái">
                        <el-option label="Đang học" value="Đang học" />
                        <el-option label="Tốt nghiệp" value="Tốt nghiệp" />
                        <el-option label="Tạm nghỉ" value="Tạm nghỉ" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Điểm TB">
                    <el-input-number v-model="editingStudent.gpa" :min="0" :max="10" :step="0.1" />
                </el-form-item>
                <el-form-item label="Ảnh đại diện">
                    <input type="file" accept="image/*" @change="onEditImageChange" />
                    <div v-if="editingStudent.profile_picture_preview || editingStudent.profile_picture" class="mt-2">
                        <img :src="editingStudent.profile_picture_preview || getProfilePictureUrl(editingStudent.profile_picture)" alt="Preview" class="w-24 h-24 object-cover rounded-full border" />
                    </div>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="showEditDialog = false">Hủy</el-button>
                <el-button type="primary" @click="updateStudent">Cập nhật</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import IconUsers from '@/assets/icons/users.svg';
import type { Student, NewStudent, EditingStudent } from '@/types/websites/student';

definePageMeta({
    layout: 'websites'
});

// Reactive data
const searchKeyword = ref('');
const selectedClass = ref('');
const selectedMajor = ref('');
const currentPage = ref(1);
const pageSize = ref(20);
const showAddDialog = ref(false);
const showViewDialog = ref(false);
const showEditDialog = ref(false);
const selectedStudent = ref<Student | null>(null);
const editingStudent = ref<EditingStudent>({} as EditingStudent);

const newStudent = ref<NewStudent>({
    studentId: '',
    fullName: '',
    email: '',
    phone: '',
    class: '',
    major: '',
});

<<<<<<< HEAD
import AcademicService from '@/services/websites/academic';

// Students data from API
const students = ref([]);

onMounted(async () => {
    try {
        const res = await AcademicService.getStudents();
        students.value = res && res.data ? res.data : res;
    } catch (error) {
        ElMessage.error('Không thể tải danh sách sinh viên');
        console.error(error);
=======
// Mock data
const students = ref<Student[]>([
    {
        id: 1,
        studentId: 'SV001',
        fullName: 'Nguyễn Văn An',
        email: 'an.nguyen@email.com',
        phone: '0123456789',
        class: 'CNTT21A',
        major: 'CNTT',
        status: 'Đang học',
        gpa: 8.5
    },
    {
        id: 2,
        studentId: 'SV002',
        fullName: 'Trần Thị Bình',
        email: 'binh.tran@email.com',
        phone: '0987654321',
        class: 'CNTT21B',
        major: 'KTPM',
        status: 'Đang học',
        gpa: 7.8
    },
    {
        id: 3,
        studentId: 'SV003',
        fullName: 'Lê Văn Cường',
        email: 'cuong.le@email.com',
        phone: '0369852147',
        class: 'CNTT22A',
        major: 'ATTT',
        status: 'Tốt nghiệp',
        gpa: 9.2
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
    }
});

// Computed properties
const totalStudents = computed(() => students.value.length);
const activeStudents = computed(() => students.value.filter(s => s.status === 'Đang học').length);
const graduatedStudents = computed(() => students.value.filter(s => s.status === 'Tốt nghiệp').length);
const suspendedStudents = computed(() => students.value.filter(s => s.status === 'Tạm nghỉ').length);

const filteredStudents = computed(() => {
    let filtered = students.value;
    
    if (searchKeyword.value) {
        filtered = filtered.filter(student => 
            student.fullName.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
            student.studentId.toLowerCase().includes(searchKeyword.value.toLowerCase())
        );
    }
    
    if (selectedClass.value) {
        filtered = filtered.filter(student => student.class === selectedClass.value);
    }
    
    if (selectedMajor.value) {
        filtered = filtered.filter(student => student.major === selectedMajor.value);
    }
    
    return filtered;
});

// Methods
const getStatusType = (status: string) => {
    switch (status) {
        case 'Đang học': return 'success';
        case 'Tốt nghiệp': return 'info';
        case 'Tạm nghỉ': return 'warning';
        default: return 'danger';
    }
};

const handleSearch = () => {
    // Search logic is handled by computed property
    ElMessage.success('Tìm kiếm hoàn tất');
};

const viewStudent = (student: Student) => {
    selectedStudent.value = student;
    showViewDialog.value = true;
};

const editStudent = (student: Student) => {
    editingStudent.value = { ...student };
    showEditDialog.value = true;
};

const editStudentFromView = () => {
    if (selectedStudent.value) {
        showViewDialog.value = false;
        editingStudent.value = { ...selectedStudent.value };
        showEditDialog.value = true;
    }
};

// Update student with image upload
const updateStudent = async () => {
    const index = students.value.findIndex(s => s.id === editingStudent.value.id);
    if (index > -1) {
<<<<<<< HEAD
        // optimistic update
        students.value[index] = { ...editingStudent.value };
        showEditDialog.value = false;
        ElMessage.success(`Cập nhật thông tin sinh viên: ${editingStudent.value.fullName}`);
        AcademicService.updateStudent(editingStudent.value.id, editingStudent.value).catch(err => {
            ElMessage.error('Cập nhật sinh viên thất bại');
            console.error(err);
        });
=======
        const formData = new FormData();
        for (const key in editingStudent.value) {
            if (key === 'profile_picture' && editingStudent.value.profile_picture instanceof File) {
                formData.append('profile_picture', editingStudent.value.profile_picture);
            } else if (key !== 'profile_picture_preview') {
                formData.append(key, String(editingStudent.value[key as keyof EditingStudent]));
            }
        }
        try {
            // Adjust API endpoint as needed
            const res = await fetch(`/api/v1/websites/students/${editingStudent.value.id}/`, {
                method: 'PUT',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: formData
            });
            if (!res.ok) throw new Error('Lỗi khi cập nhật sinh viên');
            const data = await res.json();
            students.value[index] = data;
            showEditDialog.value = false;
            ElMessage.success(`Cập nhật thông tin sinh viên: ${editingStudent.value.fullName}`);
        } catch (err) {
            ElMessage.error('Lỗi khi cập nhật sinh viên');
        }
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
    }
};

const deleteStudent = (student: any) => {
    ElMessageBox.confirm(
        `Bạn có chắc chắn muốn xóa sinh viên "${student.fullName}"?`,
        'Xác nhận xóa',
        {
            confirmButtonText: 'Xóa',
            cancelButtonText: 'Hủy',
            type: 'warning',
        }
    ).then(() => {
        const index = students.value.findIndex(s => s.id === student.id);
        if (index > -1) {
            students.value.splice(index, 1);
            ElMessage.success(`Đã xóa sinh viên: ${student.fullName}`);
        }
    }).catch(() => {
        ElMessage.info('Đã hủy xóa sinh viên');
    });
};

<<<<<<< HEAD
const addStudent = async () => {
    if (newStudent.value.studentId && newStudent.value.fullName) {
        const payload = { ...newStudent.value };
        try {
            const res = await AcademicService.createStudent(payload);
            const created = res && res.data ? res.data : res;
            // push created student or fallback
            students.value.push(created || { id: students.value.length + 1, ...payload, status: 'Đang học', gpa: 0 });
            showAddDialog.value = false;
            newStudent.value = { studentId: '', fullName: '', email: '', phone: '', class: '', major: '' };
            ElMessage.success('Thêm sinh viên thành công');
        } catch (err) {
            ElMessage.error('Thêm sinh viên thất bại');
            console.error(err);
=======
// Add student with image upload
const addStudent = async () => {
    if (newStudent.value.studentId && newStudent.value.fullName) {
        const formData = new FormData();
        for (const key in newStudent.value) {
            if (key === 'profile_picture' && newStudent.value.profile_picture instanceof File) {
                formData.append('profile_picture', newStudent.value.profile_picture);
            } else if (key !== 'profile_picture_preview') {
                formData.append(key, String(newStudent.value[key as keyof NewStudent]));
            }
        }
        try {
            // Adjust API endpoint as needed
            const res = await fetch('/api/v1/websites/students/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                },
                body: formData
            });
            if (!res.ok) throw new Error('Lỗi khi thêm sinh viên');
            const data = await res.json();
            students.value.push(data);
            showAddDialog.value = false;
            newStudent.value = {
                studentId: '',
                fullName: '',
                email: '',
                phone: '',
                class: '',
                major: '',
                profile_picture: null,
                profile_picture_preview: null
            };
            ElMessage.success('Thêm sinh viên thành công');
        } catch (err) {
            ElMessage.error('Lỗi khi thêm sinh viên');
>>>>>>> 3b3381a6d34ff10ab244e9176bf5c5305c89c0c0
        }
    } else {
        ElMessage.error('Vui lòng điền đầy đủ thông tin');
    }
};
// Helper to get full image URL from backend
const getProfilePictureUrl = (path: string | File | null | undefined) => {
    if (!path) return '';
    if (path instanceof File) return URL.createObjectURL(path);
    if (typeof path !== 'string') return '';
    if (path.startsWith('http')) return path;
    // Use relative path
    return `/media/${path}`;
};

// Handle image file change for add
const onAddImageChange = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
        newStudent.value.profile_picture = file;
        const reader = new FileReader();
        reader.onload = (ev) => {
            newStudent.value.profile_picture_preview = ev.target?.result as string;
        };
        reader.readAsDataURL(file);
    }
};

// Handle image file change for edit
const onEditImageChange = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
        editingStudent.value.profile_picture = file;
        const reader = new FileReader();
        reader.onload = (ev) => {
            editingStudent.value.profile_picture_preview = ev.target?.result as string;
        };
        reader.readAsDataURL(file);
    }
};
</script>

<style scoped>
.el-table {
    font-size: 14px;
}
</style>
