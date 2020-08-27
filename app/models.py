from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, or_, and_, DateTime
from datetime import datetime
import datetime
from sqlalchemy.orm import relationship, backref
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, logout_user, current_user
from flask import redirect
from app import db, admin


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class SanBay(db.Model):
    __tablename__ = "sanbay"

    MaSanBay = Column(String(10), primary_key=True)
    TenSanBay = Column(String(20), nullable=False)
    DiaChi = Column(String(50), nullable=True)
    ChuyenBay_SanBay = relationship('ChuyenBay_SanBay', backref="sanbay", lazy=True)

    def __str__(self):
        return self.TenSanBay


class ChuyenBay(db.Model):
    __tablename__ = "chuyenbay"

    MaChuyenBay = Column(String(10), primary_key=True)
    sanbayden_id = Column(String(10), ForeignKey(SanBay.MaSanBay), nullable=False)
    sanbaydi_id = Column(String(10), ForeignKey(SanBay.MaSanBay), nullable=False)
    NgayGio = Column(DateTime, nullable=False)
    ThoiGianBay = Column(Integer, nullable=True)
    SoLuongGheHang1 = Column(Integer, nullable=False)
    SoLuongGheHang2 = Column(Integer, nullable=False)
    PhieuDatCho = relationship('PhieuDatCho', backref='chuyenbay', lazy=True)
    SanBayTrungGian = relationship('SanBay', secondary='chuyenbay_sanbay', lazy='subquery',
                                   backref=backref('chuyenbay', lazy=True))

    def __float__(self):
        return self.MaChuyenBay


class ChuyenBay_SanBay(db.Model):
    __tablename__ = "chuyenbay_sanbay"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    MaChuyenBay = Column(String(10), ForeignKey('chuyenbay.MaChuyenBay'), primary_key=True)
    MaSanBayTrungGian = Column(String(10), ForeignKey('sanbay.MaSanBay'), primary_key=True)
    ThoiGianDung = Column(Integer, nullable=False)
    GhiChu = Column(String(50), nullable=True)


class HanhKhach(db.Model):
    __tablename__ = "hanhkhach"

    MaHanhKhach = Column(Integer, primary_key=True, autoincrement=True)
    TenHanhKhach = Column(String(50), nullable=False)
    CMND = Column(Float, nullable=True)
    SoDienThoai = Column(Float, nullable=False)
    PhieuDatCho = relationship('PhieuDatCho', backref='hanhkhach', lazy=True)

    def __str__(self):
        return self.TenHanhKhach


class DonGia(db.Model):
    __tablename__ = "dongia"

    MaDonGia = Column(Integer, primary_key=True, autoincrement=True)
    GiaTien_VND = Column(Float, nullable=False)
    PhieuDatCho = relationship('PhieuDatCho', backref='dongia', lazy=True)

    def __float__(self):
        return self.GiaTien_VND


class HangVe(db.Model):
    __tablename__ = "hangve"

    MaHangVe = Column(Integer, primary_key=True, autoincrement=True)
    TenHangVe = Column(String(50), nullable=False)
    PhieuDatCho = relationship('PhieuDatCho', backref='hangve', lazy=True)

    def __str__(self):
        return self.TenHangVe


class PhieuDatCho(db.Model):
    __tablename__ = "phieudatcho"

    MaPhieuDatCho = Column(Integer, primary_key=True, autoincrement=True)
    MaChuyenBay = Column(String(10), ForeignKey(ChuyenBay.MaChuyenBay), nullable=False)
    MaHanhKhach = Column(Integer, ForeignKey(HanhKhach.MaHanhKhach), nullable=False)
    MaHangVe = Column(Integer, ForeignKey(HangVe.MaHangVe), nullable=False)
    MaDonGia = Column(Integer, ForeignKey(DonGia.MaDonGia), nullable=False)
    NgayDat = Column(DateTime, nullable=False)
    DaMua = Column(Boolean, default=False)


class ChuyenBayModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    p = []
    d = SanBay.query.filter(SanBay.MaSanBay).all()
    print(d)
    if d:
        for a in d:
            p.append((a.MaSanBay, a.TenSanBay))
    column_labels = {'MaChuyenBay': 'Mã chuyến bay', 'sanbayden_id': 'Sân bay đến', 'sanbaydi_id': 'Sân bay đi',
                     'NgayGio': 'Ngày giờ', 'ThoiGianBay': 'Thời gian bay', 'SoLuongGheHang1': 'Số lượng ghế hạng 1',
                     'SoLuongGheHang2': 'Số lượng ghế hạng 2'}
    column_list = ('MaChuyenBay', 'sanbayden_id', 'sanbaydi_id', 'NgayGio', 'ThoiGianBay', 'SoLuongGheHang1',
                   'SoLuongGheHang2')
    form_columns = ('MaChuyenBay', 'sanbayden_id', 'sanbaydi_id', 'NgayGio',
                    'ThoiGianBay', 'SoLuongGheHang1', 'SoLuongGheHang2')


class ChuyenBay_SanBayModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    column_labels = {'ID': 'Mã', 'MaChuyenBay': 'Mã chuyến bay', 'sanbay': 'Sân bay trung gian',
                     'ThoiGianDung': 'Thời gian dừng', 'GhiChu': 'Ghi chú'}
    column_list = ('ID', 'MaChuyenBay', 'sanbay', 'ThoiGianDung', 'GhiChu')
    form_columns = ('MaChuyenBay', 'sanbay', 'ThoiGianDung', 'GhiChu')


class PhieuDatChoModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    form_columns = ('chuyenbay', 'hanhkhach', 'dongia', 'hangve', 'NgayDat', 'DaMua')


class HanhKhachModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    column_labels = {'MaHanhKhach': 'Mã hành khách', 'TenHanhKhach': 'Tên khách hàng', 'CMND': 'Chứng minh nhân dân',
                     'SoDienThoai': 'Số điện thoại'}
    form_columns = ('TenHanhKhach', 'CMND', 'SoDienThoai')


class SanBayModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    column_labels = {'MaSanBay': 'Mã sân bay', 'TenSanBay': 'Tên sân bay', 'DiaChi': 'Địa chỉ'}
    form_columns = ('MaSanBay', 'TenSanBay', 'DiaChi')


class HangVeModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    column_labels = {'MaHangVe': 'Mã hạng vé', 'TenHangVe': 'Tên hạng vé'}
    form_columns = ('TenHangVe',)


class DonGiaModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True
    column_labels = {'MaDonGia': 'Mã đơn giá', 'GiaTien_VND': 'Giá tiền(VNĐ)'}
    form_columns = ('GiaTien_VND',)


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(ChuyenBayModelView(ChuyenBay, db.session, name="Chuyến bay"))
admin.add_view(ChuyenBay_SanBayModelView(ChuyenBay_SanBay, db.session, name="Chuyến bay_Sân bay"))
admin.add_view(PhieuDatChoModelView(PhieuDatCho, db.session, name='Phiếu đặt chổ'))
admin.add_view(HanhKhachModelView(HanhKhach, db.session, name="Hành khách"))
admin.add_view(SanBayModelView(SanBay, db.session, name="Sân bay"))
admin.add_view(HangVeModelView(HangVe, db.session, name="Hạng vé"))
admin.add_view(DonGiaModelView(DonGia, db.session, name="Đơn giá"))
admin.add_view(LogoutView(name="Đăng xuất"))

if __name__ == "__main__":
    db.create_all()
