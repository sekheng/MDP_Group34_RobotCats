package com.example.robotcatmobile.home_parts;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.viewpager2.adapter.FragmentStateAdapter;

import java.util.ArrayList;

public class VPAdapter extends FragmentStateAdapter {
    ArrayList<Fragment> mFragArrayList = new ArrayList<>();

    public VPAdapter(Fragment fragment) {
        super(fragment);
    }

    @NonNull
    @Override
    public Fragment createFragment(int position) {
        return mFragArrayList.get(position);
    }

    @Override
    public int getItemCount() {
        return mFragArrayList.size();
    }

    public void addFrag(Fragment fragment) {
        mFragArrayList.add(fragment);
    }
}
